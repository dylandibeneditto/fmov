# fmov

![fmov logo](https://github.com/dylandibeneditto/fmov/blob/main/logo.png?raw=true)

![Pepy Total Downloads](https://img.shields.io/pepy/dt/fmov)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/fmov)
![GitHub Issues or Pull Requests](https://img.shields.io/github/issues/dylandibeneditto/fmov)
![PyPI - License](https://img.shields.io/pypi/l/fmov)
[![X (formerly Twitter) Follow](https://img.shields.io/twitter/follow/dylan_ditto)](https://x.com/intent/follow?screen_name=dylan_ditto)

A performant way to create rendered video with Python by leveraging `ffmpeg` and `PIL`.

[Documentation](https://dylandibeneditto.github.io/fmov/)

## Rough Benchmarks

| FPS | Resolution | Video Time | Render Time | Video Time / Render Time |
| --- | ---------- | ---------- | ----------- | --------------- |
| 1 | 1920x1080 | 30s | 0.381s | 78.74x |
| 12 | 1920x1080 | 30s | 1.995s | 15.00x |
| 24 | 1920x1080 | 30s | 3.751s | 8.00x |
| 30 | 1920x1080 | 30s | 4.541s | 6.60x |
| 60 | 1920x1080 | 30s | 8.990s | 3.34x |
| 100 | 1920x1080 | 30s | 14.492s | 2.07x |
| 120 | 1920x1080 | 30s | 17.960s | 1.67x |

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
> PIL will also be installed with fmov through pip as a dependency. (unless its already installed)