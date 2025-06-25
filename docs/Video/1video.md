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

    with Video("./output.mp4", (1920, 1080)) as video:
        
        for i in video.seconds_to_frame(30):

video = Video(path="./output.mp4", dimensions=(1920, 1080), fps=30, function=generate_frame, length="30s")
video.preview()  # Interactive preview and scrubbing
video.save()     # Render to file
```

- The `generate_frame` function describes how to create each frame.
- The `Video` object is created with the frame function and length.
- `video.preview()` allows you to interactively scrub and debug before rendering.
- `video.save()` renders the video to the output path.

<<<<<<< HEAD
=== "Traditional"

    ```py hl_lines="1 4 12"
    from fmov import Video
    from PIL import Image

    video = Video("./output.mp4", (1920, 1080))
        
    for i in video.time_to_frame("30s"):

        image = Image.new("RGB", (video.width, video.height), "#000000")

        video.pipe(image)

    video.render()
    ```

    !!! tip "Tip"

        It's recommended to use the context manager, as it allows for automatic rendering once the context has ended. However, some solutions may require the traditional method of manually calling the render function.
=======
---
>>>>>>> 35d02148043239ef723fd6612c3321cd5fcd6de2

## Parameters

When calling the `Video` function, many parameters can be tweaked. Here are all of them in order:

### `path: str = "./video.mp4"`

Specifies where the output file will be saved. Can be absolute or relative.

### `dimensions: tuple[int, int] = (1920, 1080)`
Specifies the width and height of the video.

Specifies the width and height of the video

```py title="example"
# This will create a standard 1920 x 1080 video
video = Video(dimensions=(1920, 1080))
```

### `fps: int = 30`

Specifies the frames per second of the video

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