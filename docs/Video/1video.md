# Initializing the Video

The core class of the fmov library is the `Video` class. This is where you define your video, how frames are generated, and how it is rendered.

```py
from fmov import Video
```

## Creating a Video (Modern API)

The recommended way to use fmov is to provide a frame function and a length, then preview and render:

```py title="main.py"
from fmov import Video
from PIL import Image

def generate_frame(frame: int, video: Video) -> Image:
    img = Image.new("RGB", (video.width, video.height), "#000000")
    return img

video = Video(path="./output.mp4", dimensions=(1920, 1080), fps=30, function=generate_frame, length="30s")
video.preview()  # Interactive preview and scrubbing
video.save()     # Render to file
```

- The `generate_frame` function describes how to create each frame.
- The `Video` object is created with the frame function and length.
- `video.preview()` allows you to interactively scrub and debug before rendering.
- `video.save()` renders the video to the output path.

---

## Parameters

When calling the `Video` function, many parameters can be tweaked. Here are all of them in order:

### `dimensions: tuple[int, int] = (1920, 1080)`
Specifies the width and height of the video.

### `fps: int = 30`
Specifies the frames per second of the video.

### `path: str = "./video.mp4"`
Specifies where the output file will be saved. Can be absolute or relative.

### `function: Callable[[int, Video], Image]`
A function that generates each frame. Receives the frame index and the video object.

### `length: Union[int, str]`
The length of the video, in frames or as a string (e.g. '30', '10s', '1m30s').

### `vcodec: str = "libx264"`
Specifies the video codec.
[List of supported codecs](https://ffmpeg.org/ffmpeg-codecs.html)

### `pix_fmt: str = "yuv420p"`
Specifies the pixel format.
[List of supported pixel formats](https://gist.github.com/dericed/3319386)

### `render_preset: str = "ultrafast"`
Specifies the render speed for FFmpeg.
- ultrafast
- superfast
- veryfast
- faster
- fast
- medium
- slow
- slower
- veryslow

### `crf: int = 8`
The *Constant Rate Factor* (level of compression for the vcodec).
- 0 is lossless
- 23 is default
- 51 is most compressed

### `audio_bitrate: str = "192k"`
The bitrate of the audio, essentially the quality of the sound.

### `log_duration: bool = True`
This specifies whether the Video object will print out the length it took to render.

---

!!! tip "Tip"
    The new API is recommended for most users. If you need more control, you can still use the context manager and `.pipe()` methods, but the functional API is simpler and more powerful for most workflows.