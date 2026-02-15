# Adding Audio

You can add audio events from within your frame function using the `video.audio(path, at, volume)` method. This allows you to register sound effects at any frame or timestamp, making it easy to synchronize audio with animation events.

```py title="example"
video.audio("./pop.wav", "1s")     # add sound at 1 second

video.audio("./click.mp3", 120)    # add sound at 120th frame

video.audio("./chime.m4a", "3m")   # add sound at 3 minutes

video.audio("./chime.m4a", "3m", 0.25)   # add sound at half volume
```

## `audio(path: str, at: Union(str | int), volume: float: 0.5)`

Puts a sound at a given time code. 
> To understand how time codes are evaluated, see [Converters](./2converters.md).

!!! note ""
    1.0 volume is often too loud for most applications, hence why the default volume is 0.5

## `get_audio_stamps() -> list[Audio]`
Returns the list of audio stamp objects.

## `Audio`
An internal class that can be read when calling `get_audio_stamps()`

Contains the attributes `time` (in frames), `path`, and `volume`
