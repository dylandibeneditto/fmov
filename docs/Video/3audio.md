# Adding Audio

You can add audio events from within your frame function using the `video.audio(path, at, volume)` method. This allows you to register sound effects at any frame or timestamp, making it easy to synchronize audio with animation events.

```py title="example"
from fmov import Video
from PIL import Image

video.sound("./pop.wav", "1s")     # add sound at 1 second
video.sound("./click.mp3", 120)    # add sound at 120th frame
video.sound("./chime.m4a", "3m")   # add sound at 3 minutes
```

### `sound(path: str, at: Union(str | int), volume: float: 0.4)

Puts a sound at a given time code
