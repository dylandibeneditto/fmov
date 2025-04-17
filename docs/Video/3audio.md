# Adding Audio

You can add audio at any time in your video using one of the time-based sound_at_* methods. All sound functions accept a file path and an optional volume parameter.

```py title="example"
video = Video()

video.sound_at_second(1, "./pop.wav")       # add sound at 1 second
video.sound_at_frame(120, "./click.mp3")    # add sound at 120th frame
video.sound_at_minute(0.5, "./chime.m4a")   # add sound at 30 seconds
```

### `sound_at_millisecond(time: int, path: str, volume: float = 0.4)`

Adds audio at a specific time in milliseconds.
Supports .wav, .mp3, .m4a, and many more formats.

### `sound_at_frame(frame: int, path: str, volume: float = 0.4)`

Adds audio at a specific frame index.

### `sound_at_second(time: float, path: str, volume: float = 0.4)`

Adds audio at a specific time in seconds.

### `sound_at_minute(time: float, path: str, volume: float = 0.4)`

Adds audio at a specific time in minutes.