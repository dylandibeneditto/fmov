# Introduction

**fmov** is a blazing-fast Python library for rendering videos frame-by-frame using `PIL` (Pillow), `OpenCV` or any other image generation tool (that can be converted to a Numpy array). It combines the simplicity of high-level APIs with the performance of low-level tools like FFmpeg — perfect for generative art, animations, or automated video creation.

---

## Features

- **Fast**: Built on FFmpeg for high-performance rendering.
- **Scalable**: No confusing flags or unreadable code.
- **Audio Support**: Register sound effects from within your frame function, at any frame or timestamp.
- **Helpful Utilities**: Easy time/frame conversions.
- **GPU Acceleration**: Optimized commands based on your machine
- **Modern Pythonic API**: Functional, frame-driven, and context-free.

---

## Installation

```bash
pip install fmov
```

!!! warning ""
    You must also have [FFmpeg](https://ffmpeg.org/download.html) installed on your system and available in your PATH.

```bash title="Installing FFmpeg"
sudo apt install ffmpeg     # Linux
brew install ffmpeg         # MacOS
choco install ffmpeg        # Windows
```

---

## Quick Example

```py title="hello_world.py"
from fmov import Video
from PIL import Image, ImageDraw

# using 'with Video() as video' makes rendering simpler, as when the context ends it calls render automatically
with Video(path="video.mp4", width=1920, height=1080, fps=60) as video:
    total_frames = video.time_to_frame("10s") # turns the timestamp "60s" into the number of frames in the video

    # create all the frames in the video
    for i in range(total_frames):

        # PIL stuff, just rendering out the text "Hello World"
        img = Image.new("RGB", (video.width, video.height), "#000000")
        draw = ImageDraw.Draw(img)

        draw.text(
            (100, video.height // 2),
            f"Hello world! This is frame {i}",
            fill="#ffffff"
        )

        video.add(img) # add the frame to the end of the video
```
