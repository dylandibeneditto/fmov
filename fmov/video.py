from typing import Tuple, Any
import numpy
import ffmpeg
from numpy.typing import NDArray
from fmov.audio import Audio
from PIL.Image import Image
from rich.progress import track

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
        #self.__audio_stamps: list[Audio] = []
        self.__frames: list[Image] = []
        self.__quick_image_multiplier = 2
        self.__quick_frame_multiplier = 2

    def pipe(self, image: Image):
        """
        Appends a PIL `Image` as a frame to the video

        PARAMETERS
        ---
        `image`: Image
            The image which will be appended to the video as a frame.
            Usually variables which have this type are created through
            the use of `Image.new` or `Image.open`.
            
        RAISES
        ---
        `TypeError`
            `image` is not type `PIL.Image`
        """

        if not type(image) is Image:
            raise TypeError(f"Argument of type {type(image)} cannot be assigned to type PIL.Image")

        self.__frames.append(image)

    def render(self, quick_image: bool = False, quick_frames: bool = False, log_progress: bool = True):
        """
        
        """
        image_multiplier = self.__quick_image_multiplier if quick_image else 1
        frame_multiplier = self.__quick_frame_multiplier if quick_frames else 1
        
        process = ffmpeg.input(
            "pipe:",
            format="rawvideo",
            pix_fmt="rgb24",
            s=f'{self.dimensions[0]//image_multiplier}x{self.dimensions[1]//image_multiplier}',
            framerate=self.framerate//frame_multiplier
        ).output(
            self.path,
            vcodec=self.vcodec,
            pix_fmt=self.pix_fmt,
            preset=self.render_preset,
            loglevel="quiet",
            framerate=self.framerate//frame_multiplier,
            crf=self.crf
        ).overwrite_output().run_async(pipe_stdin=True)
        
        frame_list = track(enumerate(self.__frames), "Rendering...", total=len(self.__frames)) if log_progress else enumerate(self.__frames)
        for (i, frame) in frame_list:
            if i % frame_multiplier == 0:
                final_frame = frame

                if quick_image:
                    (w, h) = frame.size
                    final_frame.resize((w//self.__quick_image_multiplier, h//self.__quick_image_multiplier))

                # convert image to bytes and pipe to ffmpeg
                process.stdin.write(numpy.array(final_frame).tobytes())
        
        # end the pipe process
        process.stdin.close()
        process.wait()

