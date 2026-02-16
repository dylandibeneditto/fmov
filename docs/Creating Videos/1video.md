# Initializing the Video

The core class of the fmov library is the `Video` class. This is where you define your video, how frames are generated, and how it is rendered.

```python
from fmov import Video
```

---

# Creating the Video
There are two methods of creating a video. Either creating the video and utilizing it's `Context Manager` or calling `video.render()` manually

=== "Context Manager"
    ```python
    from fmov import Video

    with Video("video.mp4") as video:

        for frame in total_frames
            video.add(frame_image)
    ```

=== "Traditional"
    ```python
    from fmov import Video

    video = Video("video.mp4")

    for frame in total_frames:
        video.add(frame_image)

    video.render()
    ```

As you can see, the main difference is in the fact that there is a manual `render()` call when the video should be written in the *Traditional* example. There are some cases where it is useful to be able to control when the video renders.

---

# Parameters of the Video Class

```py title="defaults"
Video(
    path: str = "./video.mp4",
    width: int = 1920,
    height: int = 1080,
    fps: int = 30,
    gpu: bool = False,
    audio_bitrate: str = "192k",
    log_duration: bool = True,
)

```

## `path: str`

> default is `./video.mp4`

This describes where the video will be written to.

---

## `width: int`

> default is `1920`

This describes the width of the video in pixels.

---

## `height: int`

> default is 1080

This descibres the height of the video in pixels.

---

## `fps: int`

> default is `30`

This describes the frames per second (framerate) of the video.

---

## `gpu: bool`

> default is `False`

This describes whether `fmov` will try to find a gpu accelerated `vcodec`.

!!! note ""
    GPU acceleration doesn't really make a difference, and can actually tend to be slower. The bottleneck for speed is the image generation code, as it is running through python. The CPU based codec `libx264` is highly optimized and GPU performance is only necessary in some cases

---

## `audio_bitrate: str`

> default is `192k`

This describes the bitrate of the audio played in the video.

---

## `log_duration: bool`

> default is `True`

This describes whether `fmov` will print out the length it took to render the video. Keep in mind this is just a number after it renders, not a progress bar.
