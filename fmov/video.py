from typing import Tuple, Any
import ffmpeg
import numpy as np
from fmov.audio import Audio
from PIL.Image import Image
import time

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
        dimensions: Tuple[int, int] = (1920, 1080),
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
        self.path = path
        self.vcodec = vcodec
        self.pix_fmt = pix_fmt
        self.render_preset = render_preset
        self.crf = crf
        self.audio_bitrate = audio_bitrate
        #self.__audio_stamps: list[Audio] = []
        self.__frame_count = 0
        self.__process = None
        self.__process_start_time = time.time() # will be set later anyways, set now to suppress errors

    def start_render(self):
        self.__process = ffmpeg.input(
            "pipe:",
            format="rawvideo",
            pix_fmt="rgb24",
            s=f"{self.width}x{self.height}",
            framerate=self.framerate
        ).output(
            self.path,
            vcodec=self.vcodec,
            pix_fmt=self.pix_fmt,
            preset=self.render_preset,
            loglevel="quiet",
            crf=self.crf
        ).overwrite_output().run_async(pipe_stdin=True)
        self.__process_start_time = time.time()

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
            self.start_render()

        frame_bytes = np.array(image, dtype=np.uint8).tobytes()
        self.__process.stdin.write(frame_bytes)
        self.__frame_count += 1

    def render(self, log_duration: bool = True):
        """Renders and outputs the final video to the determined file path
        
        Args:
            log_duration (bool): whether to print out the time it took to render on completion, default is true
        """
        if self.__process:
            self.__process.stdin.close()
            self.__process.wait()
            self.__process = None
        if log_duration:
            print(f"Completed in {time.time()-self.__process_start_time:.2f}s")

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
