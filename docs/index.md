# Introduction

**fmov** is a blazing-fast Python library for rendering videos frame-by-frame using `PIL` (Pillow). It combines the simplicity of high-level APIs with the performance of low-level tools like FFmpeg — perfect for generative art, animations, or automated video creation.

---

## Features

- **Fast**: Built on FFmpeg for high-performance rendering.
- **Simple**: Use `PIL.Image` to draw and render.
- **Scalable**: Don't worry about handling confusing flags and making code unreadable
- **Audio Support**: Add sound effects at any frame or timestamp.
- **Helpful Utilities**: Easy time/frame conversions.
- **Pythonic API**: Context manager-friendly design.

---

## Installation

```bash
pip install fmov
```

Also make sure you have [FFmpeg](https://ffmpeg.org/download.html) installed on your system

```bash
sudo apt install ffmpeg     # Linux
brew install ffmpeg         # MacOS
choco install ffmpeg        # Windows
```