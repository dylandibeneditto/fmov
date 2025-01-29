from typing import Tuple, Any
import ffmpeg
import numpy as np
from fmov.audio import Audio
from PIL.Image import Image

class Video:
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

    def pipe(self, image: Image):
        """
        Appends a PIL Image as a frame to the video

        PARAMETERS
        ---
        image: Image
            The image which will be appended to the video as a frame.
            Usually variables which have this type are created through
            the use of Image.new or Image.open.
            
        RAISES
        ---
        TypeError
            image is not type PIL.Image
        """
        if not type(image) is Image:
            raise TypeError(f"Argument of type {type(image)} cannot be assigned to type PIL.Image")

        if self.__process is None:
            self.start_render()

        frame_bytes = np.array(image, dtype=np.uint8).tobytes()
        self.__process.stdin.write(frame_bytes)
        self.__frame_count += 1

    def render(self):
        if self.__process:
            self.__process.stdin.close()
            self.__process.wait()
            self.__process = None

    def seconds_to_frame(self, time: float) -> int:
        return int(time * self.framerate)

    def minutes_to_frame(self, time: float) -> int:
        return self.seconds_to_frame(time*60)

    def milliseconds_to_frame(self, time: int) -> int:
        return self.seconds_to_frame(time/1000)
