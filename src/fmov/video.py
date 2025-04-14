import ffmpeg
import numpy as np
from PIL.Image import Image
import time
import subprocess
import os
import shutil

class Video:
    """fmov.Video
    
    Args:
        dimensions (Tuple[int, int]): The dimensions of the video, `(w, h)`
        framerate (int): The framerate of the video
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
        framerate: int = 30,
        path: str = "./video.mp4",
        vcodec: str = "libx264",
        pix_fmt: str = "yuv420p",
        render_preset: str = "ultrafast",
        crf: int = 8,
        audio_bitrate: str = "192k"
    ):
        self.width = dimensions[0]
        self.height = dimensions[1]
        self.framerate = framerate
        self.__path = path
        self.__temp_path = self.__get_temp_path(path)
        self.vcodec = vcodec
        self.pix_fmt = pix_fmt
        self.render_preset = render_preset
        self.crf = crf
        self.audio_bitrate = audio_bitrate
        self.__audio_stamps: set[tuple[int, str, float]] = set([])
        """tuple index meanings:
            0 (int): time in ms of the audio
            1 (str): path to the sound effect
            2 (float): volume of the sound effect 0 - 1
        """
        self.__frame_count = 0
        self.__process = None
        self.__process_start_time = time.time() # will be set later anyways, set now to suppress errors

    def __start_render(self):
        self.__process = ffmpeg.input(
            "pipe:",
            format="rawvideo",
            pix_fmt="rgb24",
            s=f"{self.width}x{self.height}",
            framerate=self.framerate
        ).output(
            self.__temp_path,
            vcodec=self.vcodec,
            pix_fmt=self.pix_fmt,
            preset=self.render_preset,
            loglevel="quiet",
            crf=self.crf
        ).overwrite_output().run_async(pipe_stdin=True)
        self.__process_start_time = time.time()

    def sound_at_millisecond(self, time: int, path: str, volume: float = 0.4):
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

        self.__audio_stamps.add((int(time), str(path), max(float(volume),0.0)))

    def sound_at_frame(self, frame: int, path: str, volume: float = 0.4):
        """Inserts a sound at `n` frames
        
        Args:
            frame (int): frame to insert the sound
            path (str): path to the audio file
            volume (float): volume of the audio (between 0.0-1.0)

        Raises:
            FileNotFoundError: path to audio file does not exist
        """

        self.sound_at_millisecond(self.frame_to_milliseconds(frame), path, volume)

    def sound_at_second(self, time: float, path: str, volume: float = 0.4):
        """Inserts a sound at `n` seconds
        
        Args:
            time (float): time in seconds
            path (str): path to the audio file
            volume (float): volume of the audio (between 0.0-1.0)

        Raises:
            FileNotFoundError: path to audio file does not exist
        """

        self.sound_at_millisecond(int(time*1000), path, volume)

    def sound_at_minute(self, time: float, path: str, volume: float = 0.4):
        """Inserts a sound at `n` minutes
        
        Args:
            time (float): time in minutes
            path (str): path to the audio file
            volume (float): volume of the audio (between 0.0-1.0)

        Raises:
            FileNotFoundError: path to audio file does not exist
        """

        self.sound_at_second(time*60, path, volume)

    def pipe(self, image: Image):
        """Appends a PIL `Image` as a frame to the video

        Args:
            image (Image): The image which will be appended to the video as a frame
            
        Raises:
            TypeError: `image` is not type `PIL.Image`
        """
        if not type(image) is Image:
            raise TypeError(f"Argument of type {type(image)} cannot be assigned to type PIL.Image")

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

    def render(self, prompt_deletion: bool = True, log_duration: bool = True):
        """Renders and outputs the final video to the determined file path
        
        Args:
            log_duration (bool): whether to print out the time it took to render on completion, default is true
            prompt_deletion (bool): prompts the user whether they want to delete the temporary file... make sure everything is right before this is disabled
        """
        if self.__process:
            self.__process.stdin.close()
            self.__process.wait()
            self.__process = None
            if len(self.__audio_stamps) > 0:
                self.__attach_audio()
            else:
                shutil.copy(self.__temp_path, self.__path)
        if log_duration:
            print(f"Completed in {time.time()-self.__process_start_time:.2f}s")
        if prompt_deletion:
            prompt = input(f"Would you like to delete '{self.__temp_path}'? Y/n ")
            if "Y" not in prompt:
                return
            print(f"Deleting {self.__temp_path}...")
        os.remove(self.__temp_path)

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

        return int(time * self.framerate)

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

        return int(frame/self.framerate * 1000)

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

    def __repr__(self):
        return f"fmov.Video({self.width}, {self.height}, {self.framerate}, {self.__path})"
    
    def __str__(self):
        return f"Video at {self.__path} with dimensions {self.width}x{self.height} at {self.framerate}fps"