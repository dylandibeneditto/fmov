from typing import Tuple

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
        self.dimensions = dimensions
        self.framerate = framerate
        self.path = path
        self.vcodec = vcodec
        self.pix_fmt = pix_fmt
        self.render_preset = render_preset
        self.crf = crf
        self.audio_bitrate = audio_bitrate
        self.__audio_stamps: list[Audio] = []
        self.__frames: list[NDArray[Any]] = []
