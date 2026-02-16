# fmov

![fmov logo](https://github.com/dylandibeneditto/fmov/blob/main/logo.png?raw=true)

![Pepy Total Downloads](https://img.shields.io/pepy/dt/fmov)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/fmov)
![GitHub Issues or Pull Requests](https://img.shields.io/github/issues/dylandibeneditto/fmov)
![PyPI - License](https://img.shields.io/pypi/l/fmov)

The fastest video-creation library in Python. Support for sound effects, `PIL`, and `OpenCV` image generation.

[Documentation](https://dylandibeneditto.github.io/fmov/)

## Rough Benchmarks from [this example](examples/opencv)

| FPS | Resolution | Video Time | Render Time |
| --- | ---------- | ---------- | ----------- |
| 1 | 1920x1080 | 30s | 0.25s |
| 12 | 1920x1080 | 30s | 1.74s |
| 24 | 1920x1080 | 30s | 4.08s |
| 30 | 1920x1080 | 30s | 4.99s |
| 60 | 1920x1080 | 30s | 9.64s |
| 100 | 1920x1080 | 30s | 16.02s |
| 120 | 1920x1080 | 30s | 19.09s |

---

https://github.com/user-attachments/assets/1bbe2acc-e563-4fa4-bbf0-b0e6f04f0016

> Here's an example use of fmov for automated chess analysis videos (trimmed to 1:30 to allow for embedding)

## Installing

Install fmov via pip:

```bash
pip install fmov
```

### Dependencies

Make sure to have ffmpeg installed on your system and executable from the terminal

```bash
sudo apt install ffmpeg     # Linux
brew install ffmpeg         # MacOS
choco install ffmpeg        # Windows
```

[Downloading FFmpeg](https://ffmpeg.org/download.html)

> [!NOTE]
> `PIL` will be installed automatically, if you would like to use `OpenCV`, install it manually
