# Time & Frame Conversions

fmov provides a set of helpful utilities for converting between frames and time units. This makes it easy to synchronize animation, audio, and effects.

```py title="example"
video = Video(fps=30)

video.time_to_frame("2s") # 60
video.frame_to_seconds(60) # 2
```

### `time_to_frame(time: Union(str | int)) -> int`

Returns the frames for a given time code

```py title="time_codes"
video = Video(fps=30)

video.time_to_frame("1m") # 1800
video.time_to_frame("1m 30s") # 2700
video.time_to_frame("3h 10m 25s 500ms") # 342765
video.time_to_frame(10) # 10
```

### `frame_to_milliseconds(frame: int) -> int`
Returns the time in milliseconds that the given frame will begin.

### `frame_to_seconds(frame: int) -> float`
Returns the time in seconds that the given frame will begin.

### `frame_to_minutes(frame: int) -> float`
Returns the time in minutes that the given frame will begin.