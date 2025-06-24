# Introduction

**fmov** is a blazing-fast Python library for rendering videos frame-by-frame using `PIL` (Pillow). It combines the simplicity of high-level APIs with the performance of low-level tools like FFmpeg — perfect for generative art, animations, or automated video creation.

---

## Features

- **Fast**: Built on FFmpeg for high-performance rendering.
- **Simple**: Use `PIL.Image` to draw and render.
- **Scalable**: No confusing flags or unreadable code.
- **Audio Support**: Register sound effects from within your frame function, at any frame or timestamp.
- **Interactive Preview**: Scrub, play, and debug your animation before rendering.
- **Helpful Utilities**: Easy time/frame conversions.
- **Modern Pythonic API**: Functional, frame-driven, and context-free.

---

## Installation

```bash
pip install fmov
```

You must also have [FFmpeg](https://ffmpeg.org/download.html) installed on your system and available in your PATH.

```bash
sudo apt install ffmpeg     # Linux
brew install ffmpeg         # MacOS
choco install ffmpeg        # Windows
```

---

## Quick Example

```python
from fmov import Video
from PIL import Image

def generate_frame(frame: int, video: Video) -> Image:
    img = Image.new("RGB", (video.width, video.height), "#000000")
    return img

video = Video(path="output.mp4", dimensions=(1920, 1080), fps=30, function=generate_frame, length="5s")
video.preview()  # Interactive preview
video.save()     # Render to file
```