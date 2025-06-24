import ffmpeg
import numpy as np
from PIL.Image import Image
import time
import subprocess
import os
import shutil
import cv2
from PIL import Image
from rich.progress import track

class Video:
    """fmov.Video
    
    Args:
        dimensions (Tuple[int, int]): The dimensions of the video, `(w, h)`
        fps (int): The fps of the video
        path (str): The file path which the image will be outputted into
        vcodec (str): See ffmpeg `vcodec`, default is 'libx265'
        pix_fmt (str): See ffmpeg `pix_fmt`, default is 'yuv420p'
        render_preset (str): See ffmpeg `preset`, default is 'ultrafast'
        crf (str): See ffmpeg `crf`, default is 8
        audio_bitrate (str): See ffmpeg `bitrate`, default is '192k'
    """
    def __init__(
        self,
        dimensions: tuple[int, int] = (1920, 1080),
        fps: int = 30,
        path: str = "./video.mp4",
        vcodec: str = "libx264",
        pix_fmt: str = "yuv420p",
        render_preset: str = "ultrafast",
        crf: int = 8,
        audio_bitrate: str = "192k",
        log_duration: bool = True,
        function=None,
        length=None
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
        self.__frame_count = 0
        self.__process_start_time = time.time() # will be set later anyways, set now to suppress errors
        self.function = function
        self.length = self._parse_length(length)
        self._audio_stamps = []

    def _parse_length(self, length):
        """
        Parses a length string or int into a number of frames (for self.frames).
        Supports frames (no suffix), ms, s, m, h, and stacked units (e.g. '1h23m', '2m 10s', '500ms', '100').
        """
        if length is None:
            return 0
        if isinstance(length, int):
            # Assume frames if int
            return length
        if isinstance(length, str):
            import re
            total_frames = 0.0
            length = length.replace(' ', '')
            for value, unit in re.findall(r'([\d.]+)(ms|s|m|h|)', length):
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

    def audio(self, path: str, at, volume: float = 1.0):
        at = self._parse_length(str(at))
        self.__sound_at_millisecond(float(at) / self.fps * 1000.0, path, volume)

    def __sound_at_millisecond(self, time: int, path: str, volume: float = 0.4):
        """Inserts a sound at `n` milliseconds
        
        Args:
            time (int): time in milliseconds
            path (str): path to the audio file
            volume (float): volume of the audio (between 0.0-1.0)

        Raises:
            FileNotFoundError: path to audio file does not exist
        """
        if not os.path.exists(path):
            raise FileNotFoundError(f"audio file '{path}' does not exist")

        self.__audio_stamps.append((int(time), str(path), max(float(volume),0.0)))

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

    def time_to_frame(self, time: str) -> int:
        return self._parse_length(time)

    def seconds_to_frame(self, time: float) -> int:
        """Finds the frame which will be showing at `n` seconds

        Args:
            time (float): the time in seconds expressed as a float

        Raises:
            ValueError: `time` is not assignable to type `float`

        Returns:
            int: the frame in the video at `n` seconds
        """
        time = float(time)

        return int(time * self.fps)

    def minutes_to_frame(self, time: float) -> int:
        """Finds the frame which will be showing at `n` minutes

        Args:
            time (float): the time in minutes expressed as a float

        Raises:
            ValueError: `time` is not assignable to type `float`

        Returns:
            int: the frame in the video at `n` minutes
        """
        return self.seconds_to_frame(time*60)

    def milliseconds_to_frame(self, time: int) -> int:
        """Finds the frame which will be showing at `n` milliseconds

        Args:
            time (int): the time in milliseconds expressed as a int

        Raises:
            ValueError: `time` is not assignable to type `float`

        Returns:
            int: the frame in the video at `n` milliseconds
        """
        return self.seconds_to_frame(time/1000)

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

    def preview(self):
        """Preview video by generating frames on the fly and allowing scrubbing. Uses PyQt5 for advanced interactivity."""
        from .previewer import preview_video
        preview_video(self.length, self.function, self)

    def save(self, use_preview_cache=True, workers=0):
        """Render and save the video using the frame function. Optionally use preview cache and multiprocessing."""
        if not self.function or not self.length:
            raise ValueError("No frame generation function or length specified.")

        self.__process_start_time = time.time()
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(self.__temp_path, fourcc, self.fps, (self.width, self.height))

        frame_cache = None
        if use_preview_cache:
            try:
                from .previewer import VideoPreviewer
                if hasattr(self, '_previewer_instance') and hasattr(self._previewer_instance, 'frame_cache'):
                    frame_cache = self._previewer_instance.frame_cache
            except Exception:
                frame_cache = None

        def get_frame(i):
            if frame_cache and i in frame_cache:
                arr = frame_cache[i]
            else:
                img = self.function(i, self)
                if not isinstance(img, Image.Image):
                    raise TypeError("Frame function must return a PIL.Image")
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                arr = np.array(img)
            return arr[..., ::-1]

        for i in (range(self.length) if not self.log_duration else track(range(self.length), description="Generating Video...", total=self.length)):
            arr = get_frame(i)
            out.write(arr)
        out.release()

        if len(self.__audio_stamps) > 0:
            self.__attach_audio()
        else:
            shutil.copy(self.__temp_path, self.__path)
        if self.log_duration:
            print(f"Completed in {time.time()-self.__process_start_time:.2f}s")
        os.remove(self.__temp_path)