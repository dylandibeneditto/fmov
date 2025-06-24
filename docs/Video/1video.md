# Initializing the Video

The core class of the fmov library is the `Video` class. This class is where video is created, piped to, and finally rendered.

```py
from fmov import Video
```

## Creating the Video object

=== "Context Manager"

    ```py hl_lines="1 4"
    from fmov import Video
    from PIL import Image

    with Video((1920, 1080), path="./output.mp4") as video:
        
        for i in video.seconds_to_frame(30):

            image = Image.new("RGB", (video.width, video.height), "#000000")

            video.pipe(image)
    ```

=== "Traditional"

    ```py hl_lines="1 4 12"
    from fmov import Video
    from PIL import Image

    video = Video((1920, 1080), path="./output.mp4"):
        
    for i in video.seconds_to_frame(30):

        image = Image.new("RGB", (video.width, video.height), "#000000")

        video.pipe(image)

    video.render()
    ```

    !!! tip "Tip"

        It's recommended to use the context manager, as it allows for automatic rendering once the context has ended. However, some solutions may require the traditional method of manually calling the render function.

## Parameters

When calling the `Video` function, many parameters can be tweaked. Here are all of them in order:

### `dimensions: tuple[int, int] = (1920, 1080)`

Specifies the width and height of the video

```py title="example"
# This will create a standard 1920 x 1080 video
video = Video(dimensions=(1920, 1080))
```

### `fps: int = 30`

Specifies the frames per second of the video

### `path: str = "./video.mp4"`

Specifies where the output file will be saved. Can be absolute or relative.

### `vcodec: str = "libx264"`

Specifies the video codec

[List of supported codecs](https://ffmpeg.org/ffmpeg-codecs.html)

### `pix_fmt: str = "yuv420p"`

Specifies the pixel format

[List of supported pixel formats](https://gist.github.com/dericed/3319386)

### `render_preset: str = "ultrafast"`

Specifies the render speed for FFmpeg

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

The *Constant Rate Factor*

Specifies the level of compression done by the vcodec

If you are using `libx264`:

- 0 is lossless
- 23 is default
- 51 is most compressed

### `audio_bitrate: str = "192k"`

The bitrate of the audio, essentially the quality of the sound.

192k is usually standard for lossless audio bitrates.

### `prompt_deletion: bool = True`

This specifies whether you will be prompted to delete the temporary file.

!!! warning "Warning"

    When set to false, make sure you don't have any important files that could possibly be deleted if an error occurs (although that event is **severly** unlikely)

### `log_duration: bool = True`

This specifies whether the Video object will print out the length it took to render.