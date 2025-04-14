# fmov

![fmov logo](https://github.com/dylandibeneditto/fmov/blob/main/logo.png?raw=true)

A performant way to create rendered video with Python by leveraging `ffmpeg` and `PIL`.

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

## Tutorial

***The code for this and more examples can be found in the [examples](https://github.com/dylandibeneditto/fmov/tree/main/examples) folder***

Starting the `Video`:

```python
from fmov import Video

with Video((1920, 1080), framerate=120, path="./video.mp4", prompt_deletion=False) as video:
```

> [!NOTE]
> Anytime the program has to delete the temporary file, fmov will prompt the user unless `prompt_deletion` is disabled as an argument in the `Video` class.

Creating frames:

```python
    # some code to make a 30 second video displaying the index of each frame

    for i in range(video.seconds_to_frame(30)):
        img = Image.new("RGB", (video.width, video.height), "#000000")
        draw = ImageDraw.Draw(img)

        #          x    y                 content of the text                     color
        draw.text((100, video.height//2), f"Hello world! This is frame {str(i)}", fill="#ffffff")

        video.pipe(img)
```

Adding SFX:

```python
    video.sound_at_frame(frame=10, path="./audio.mp3", volume=0.5)

    video.sound_at_millisecond(time=4000, path="./audio.wav", volume=1.0)

    video.sound_at_second(time=25, path="./audio.m4a")
```
