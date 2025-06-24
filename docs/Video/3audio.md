# Adding Audio

You can add audio events from within your frame function using the `video.audio(path, at, volume)` method. This allows you to register sound effects at any frame or timestamp, making it easy to synchronize audio with animation events.

```py title="example"
from fmov import Video
from PIL import Image

def generate_frame(frame: int, video: Video) -> Image:
    if frame % 30 == 0:
        video.audio("./pop.wav", at=frame, volume=1.0)  # Add sound at every second
    img = Image.new("RGB", (video.width, video.height), "black")
    return img

video = Video(path="output.mp4", dimensions=(640, 480), fps=30, function=generate_frame, length="5s")
video.preview()
video.save()
```

### `video.audio(path: str, at, volume: float = 1.0)`

Adds audio at a specific frame or time. The `at` argument can be a frame index, or a string like `'2s'`, `'500ms'`, `'1m30s'`, etc.

- `path`: Path to the audio file (wav, mp3, m4a, etc.)
- `at`: When to play the sound (frame number or time string)
- `volume`: Volume of the sound (0.0 to 1.0, default 1.0)

!!! note
    You can call `video.audio(...)` as many times as you want, even multiple times per frame.