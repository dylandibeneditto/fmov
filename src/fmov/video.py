import ffmpeg
import numpy as np
import shutil
import os
import time
import re
from PIL.Image import Image
import subprocess
from .audio import Audio
from .vcodec import pick_vcodec, get_vcodec_settings

class Video:
    
    def __init__(
        self,
        path: str = "./video.mp4",
        width: int = 1920,
        height: int = 1080,
        fps: int = 30,
        gpu: bool = False,
        audio_bitrate: str = "192k",
        log_duration: bool = True,
    ):
        self.width: int = width
        self.height: int = height
        self.fps: int = fps
        self.__path: str = path
        self.__temp_path: str = self.__get_temp_path(path)

        self.__vcodec: str = pick_vcodec(gpu)
        self.vcodec: dict = get_vcodec_settings(self.__vcodec)

        self.audio_bitrate = audio_bitrate
        self.__audio_stamps: list[Audio] = list([])

        self.log_duration = log_duration


        self.__process = None
        self.__frame_count = 0
        self.__process_start_time = None

    
    #
    # CONTEXT MANAGER
    #
    def __enter__(self):
        if self.__process is None:
            self.__start_render()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.__process:
            self.render()
        else:
            raise ValueError("No process was created to render")

    #
    # RENDERING
    #
    def __start_render(self):
        stream = ffmpeg.input( # build the ffmpeg pipe
            "pipe:",
            format="rawvideo",
            pix_fmt="rgb24",
            s=f"{self.width}x{self.height}",
            framerate=self.fps
        )

        # compile list of output arguments
        output_args = self.vcodec.copy()
        output_args.pop("name")
        output_args["pix_fmt"] = "yuv420p"
        output_args["loglevel"] = "error"

        self.__process = ( # start the process
            stream.output(self.__temp_path, **output_args)
                .overwrite_output()
                .run_async(pipe_stdin=True)
        )

        self.__process_start_time = time.time()

    def render(self) -> None:
        if self.__process:
            self.__process.stdin.close()
            self.__process.wait()
            self.__process = None
            if len(self.__audio_stamps) > 0:
                self.__attach_audio() # attach the audio to the video
            else:
                shutil.copy(self.__temp_path, self.__path) # rename the file if theres no audio
        else:
            raise ValueError("Tried to render before a process was created")
        if self.log_duration and self.__process_start_time:
            print(f"Completed in {time.time()-self.__process_start_time:.2f}s")
        os.remove(self.__temp_path)

    #
    # AUDIO / SOUND EFFECTS
    #
    def audio(self, path: str, at: str | int, volume: float = 0.5) -> None:
        t: int = self.time_to_frame(at)
        self._audio_at_ms(t // int(self.fps * 1000), path, volume)
    
    def _audio_at_ms(self, time: int, path: str, volume: float) -> None:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Audio file '{path}' does not exist")
        self.__audio_stamps.append(Audio(
            int(time),
            str(path),
            min(max(float(volume),0.0),1.0)
        ))

    def __attach_audio(self) -> None:
        cmd = ["ffmpeg", "-y", "-i", self.__temp_path]

        filter_complex_parts = []
        amix_inputs = []

        for i, sound in enumerate(self.__audio_stamps):

            cmd.extend(["-i", sound.path])

            audio_label = f"[{i + 1}:a]"
            delayed_audio = f"{audio_label} volume={sound.volume},adelay={sound.time}|{sound.time} [delayed{i}]"
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
            "-b:a", self.audio_bitrate,
            "-loglevel", "error",
            self.__path
        ])

        subprocess.run(cmd, check=True)

    #
    # ADD FRAME
    #
    def add(self, image):
        """
        Accepts PIL.Image, OpenCV / Numpy array, and raw RGB byte data

        image: Image | np.ndarray | bytes | bytearray
        """
        if isinstance(image, np.ndarray):

            if image.dtype != np.uint8:
                image = image.astype(np.uint8, copy=False)

            if image.ndim == 2:
                image = np.repeat(image[:, :, None], 3, axis=2)

            elif image.shape[2] == 4:
                image = image[:, :, :3]

            if not image.flags['C_CONTIGUOUS']:
                image = np.ascontiguousarray(image)

            image_bytes = memoryview(image)

        elif isinstance(image, Image):
            image = np.asarray(image)
            if not image.flags['C_CONTIGUOUS']:
                image = np.ascontiguousarray(image)
            image_bytes = memoryview(image)

        elif isinstance(image, (bytes, bytearray, memoryview)):
            image_bytes = image

        else:
            raise TypeError(f"Unsupported image object type: {type(image)}")

        if not self.__process:
            raise ValueError("No process was created to add frames")

        self.__process.stdin.write(image_bytes)
        self.__frame_count += 1

    #
    # TIME HELPERS
    #

    # times -> frame

    def time_to_frame(self, t: str | int) -> int:
        """
        Parses a time string or int into a number of frames (for self.frames).
        Supports frames (no suffix), ms, s, m, h, and stacked units (e.g. '1h23m', '2m 10s', '500ms', '5s 10').
        """
        if isinstance(t, int):
            return t
        if isinstance(t, str):
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


    # frames -> time

    def frame_to_milliseconds(self, frame: int) -> int:
        return int(frame/self.fps * 1000)
    
    def frame_to_seconds(self, frame: int) -> float:
        return self.frame_to_milliseconds(frame) / 1000

    def frame_to_minutes(self, frame: int) -> float:
        return self.frame_to_seconds(frame) / 60

    def frame_to_hours(self, frame: int) -> float:
        return self.frame_to_minutes(frame) / 60

    #
    # GETTERS AND SETTERS
    #
    def __get_temp_path(self, path: str) -> str:
        extension = "."+(path.split(".")[-1])
        return path[:-len(extension)]+".tmp"+extension

    def set_path(self, path: str):
        self.__path = path
        self.__temp_path = self.__get_temp_path(path)

    def get_path(self) -> str:
        return self.__path

    def get_audio_stamps(self) -> list[Audio]:
        return self.__audio_stamps

    def set_vcodec(self, vcodec: str):
        self.__vcodec = vcodec
        self.vcodec = get_vcodec_settings(vcodec)

    def __repr__(self) -> str:
        return f"fmov.Video({self.width}, {self.height}, {self.fps}, {self.__path})"
    
    def __str__(self) -> str:
        return f"Video at {self.__path} with dimensions {self.width}x{self.height} at {self.fps}fps"
