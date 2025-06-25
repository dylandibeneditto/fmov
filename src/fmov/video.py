import ffmpeg
import numpy as np
from PIL.Image import Image
import time
import subprocess
import os
import shutil
import cv2

class Video:
    """fmov.Video
    
    Args:
        path (str): The file path which the image will be outputted into
        dimensions (Tuple[int, int]): The dimensions of the video, `(w, h)`
        fps (int): The fps of the video
        vcodec (str): See ffmpeg `vcodec`, default is 'libx265'
        pix_fmt (str): See ffmpeg `pix_fmt`, default is 'yuv420p'
        render_preset (str): See ffmpeg `preset`, default is 'ultrafast'
        crf (int): See ffmpeg `crf`, default is 8
        audio_bitrate (str): See ffmpeg `bitrate`, default is '192k'
    """
    def __init__(
        self,
        path: str = "./output.mp4",
        dimensions: tuple[int, int] = (1920, 1080),
        fps: int = 30,
        vcodec: str = "libx264",
        pix_fmt: str = "yuv420p",
        render_preset: str = "ultrafast",
        crf: int = 8,
        audio_bitrate: str = "192k",
        log_duration: bool = True
    ):
        self.width = dimensions[0]
        self.height = dimensions[1]
        self.fps = fps
        self.__path = path
        self.__temp_path = self.__get_temp_path(path)
        self.vcodec = vcodec
        self.pix_fmt = pix_fmt
        self.render_preset = render_preset
        self.crf = crf
        self.audio_bitrate = audio_bitrate
        self.log_duration = log_duration
        self.__audio_stamps: list[tuple[int, str, float]] = list([])
        """tuple index meanings:
            0 (int): time in ms of the audio
            1 (str): path to the sound effect
            2 (float): volume of the sound effect 0 - 1
        """
        self.__process = None
        self.__frame_count = 0
        self.__process_start_time = time.time() # will be set later anyways, set now to suppress errors

    def __enter__(self):
        if self.__process is None:
            self.__start_render()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        if self.__process:
            self.render()

    def __start_render(self):
        self.__process = ffmpeg.input(
            "pipe:",
            format="rawvideo",
            pix_fmt="rgb24",
            s=f"{self.width}x{self.height}",
            framerate=self.fps
        ).output(
            self.__temp_path,
            vcodec=self.vcodec,
            pix_fmt=self.pix_fmt,
            preset=self.render_preset,
            loglevel="error",
            crf=self.crf
        ).overwrite_output().run_async(pipe_stdin=True)
        self.__process_start_time = time.time()

    def audio(self, path: str, at, volume: float = 1.0):
        at = self._parse_length(str(at))
        self.__sound_at_millisecond(float(at) / self.fps * 1000.0, path, volume)

    def _parse_time(self, t):
        """
        Parses a time string or int into a number of frames (for self.frames).
        Supports frames (no suffix), ms, s, m, h, and stacked units (e.g. '1h23m', '2m 10s', '500ms', '100').
        """
        if t is None:
            return 0
        if isinstance(t, int):
            # Assume frames if int
            return t
        if isinstance(t, str):
            import re
            total_frames = 0.0
            t = t.replace(' ', '')
            for value, unit in re.findall(r'([\d.]+)(ms|s|m|h|)', t):
                if unit == '':  # frames
                    total_frames += float(value)
                elif unit == 'ms':
                    total_frames += float(value) * self.fps / 1000.0
                elif unit == 's':
                    total_frames += float(value) * self.fps
                elif unit == 'm':
                    total_frames += float(value) * 60 * self.fps
                elif unit == 'h':
                    total_frames += float(value) * 3600 * self.fps
            return int(total_frames)
        return 0

    def time_to_frame(self, time: str | int):
        return self._parse_time(time)

    def sound(self, path: str, at: str | int, volume: float = 0.4):
        """Inserts a sound at a time code
        
        Args:
            time (int): timecode (1m 30s, 1h 10m, 100, 500ms)
            path (str): path to the audio file
            volume (float): volume of the audio (between 0.0-1.0)

        Raises:
            FileNotFoundError: path to audio file does not exist
        """
        self._sound_at_millisecond(self.frame_to_milliseconds(self._parse_time(at)), path, volume)

    def _sound_at_millisecond(self, time: int, path: str, volume: float = 0.4):
        if not os.path.exists(path):
            raise FileNotFoundError(f"audio file '{path}' does not exist")
        self.__audio_stamps.append((int(time), str(path), max(float(volume),0.0)))

    def pipe(self, image: Image):
        """Appends a PIL `Image` as a frame to the video

        Args:
            image (Image): The image which will be appended to the video as a frame
            
        Raises:
            TypeError: `image` is not type `PIL.Image`
        """
        if not type(image) is Image:
            raise TypeError(f"Argument of type {type(image)} cannot be assigned to type PIL.Image")
        if image.size != (self.width, self.height):
            raise ValueError(f"Image size {image.size} does not match video size {(self.width, self.height)}")
        if image.mode != "RGB":
            raise ValueError(f"Image mode {image.mode} is not 'RGB'")

        if self.__process is None:
            self.__start_render()

        frame_bytes = np.array(image, dtype=np.uint8).tobytes()
        self.__process.stdin.write(frame_bytes)
        self.__frame_count += 1

    def __attach_audio(self):
        cmd = ["ffmpeg", "-y", "-i", self.__temp_path]

        filter_complex_parts = []
        amix_inputs = []

        for i, sound in enumerate(self.__audio_stamps):

            cmd.extend(["-i", sound[1]])

            audio_label = f"[{i + 1}:a]"
            delayed_audio = f"{audio_label} volume={sound[2]},adelay={sound[0]}|{sound[0]} [delayed{i}]"
            filter_complex_parts.append(delayed_audio)
            amix_inputs.append(f"[delayed{i}]")

        amix_filter = f"{''.join(amix_inputs)} amix=inputs={len(amix_inputs)}:duration=longest:normalize=0 [mixed_audio]"
        filter_complex_parts.append(amix_filter)

        filter_complex_parts.append("[mixed_audio] aresample=async=1000 [audio_out]")

        filter_complex = "; ".join(filter_complex_parts)

        cmd.extend([
            "-filter_complex", filter_complex,
            "-map", "0:v",
            "-map", "[audio_out]",
            "-c:v", "copy",
            "-c:a", "aac",
            "-b:a", "192k",
            "-loglevel", "quiet",
            self.__path
        ])

        subprocess.run(cmd, check=True)

    def render(self):
        """Renders and outputs the final video to the determined file path"""

        if self.__process:
            self.__process.stdin.close()
            self.__process.wait()
            self.__process = None
            if len(self.__audio_stamps) > 0:
                self.__attach_audio()
            else:
                shutil.copy(self.__temp_path, self.__path)
        if self.log_duration:
            print(f"Completed in {time.time()-self.__process_start_time:.2f}s")
        os.remove(self.__temp_path)

    def frame_to_milliseconds(self, frame: int) -> int:
        """Finds the time in milliseconds that the `n`th frame will begin at
        
        Args:
            frame (int): the frame where the time will be found

        Raises:
            ValueError: `frame` is not assignable to type `int`

        Returns:
            int: the time in milliseconds where the frame started
        """
        frame = int(frame)

        return int(frame/self.fps * 1000)

    def frame_to_seconds(self, frame: int) -> float:
        """Finds the time in seconds that the `n`th frame will begin at
        
        Args:
            frame (int): the frame where the time will be found

        Raises:
            ValueError: `frame` is not assignable to type `int`

        Returns:
            float: the time in seconds where the frame started
        """

        return self.frame_to_milliseconds(frame) / 1000

    def frame_to_minutes(self, frame: int) -> float:
       """Finds the time in minutes that the `n`th frame will begin at
       
       Args:
           frame (int): the frame where the time will be found

       Raises:
           ValueError: `frame` is not assignable to type `int`

       Returns:
           float: the time in minutes where the frame started
       """

       return self.frame_to_seconds(frame) / 60

    def __get_temp_path(self, path: str):
        extension = "."+(path.split(".")[-1])
        return path[:-len(extension)]+".tmp"+extension

    def set_path(self, path: str):
        self.__path = path
        self.__temp_path = self.__get_temp_path(path)

    def get_path(self):
        return self.__path

    def get_audio_stamps(self):
        return self.__audio_stamps

    def __repr__(self):
        return f"fmov.Video({self.width}, {self.height}, {self.fps}, {self.__path})"
    
    def __str__(self):
        return f"Video at {self.__path} with dimensions {self.width}x{self.height} at {self.fps}fps"
