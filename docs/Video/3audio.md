# Adding Audio

You can add audio at any time in your video using one of the time-based sound_at_* methods. All sound functions accept a file path and an optional volume parameter.

```py title="example"
video = Video()

video.sound("./pop.wav", "1s")     # add sound at 1 second
video.sound("./click.mp3", 120)    # add sound at 120th frame
video.sound("./chime.m4a", "3m")   # add sound at 3 minutes
```

### `sound(path: str, at: Union(str | int), volume: float: 0.4)

Puts a sound at a given time code