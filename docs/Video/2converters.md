# Time & Frame Conversions

fmov provides a set of helpful utilities for converting between frames and time units. This makes it easy to synchronize animation, audio, and effects.

```py title="example"
from fmov import Video

video = Video(fps=30)

video.seconds_to_frame(2)      # 60
video.frame_to_seconds(60)     # 2.0
video.minutes_to_frame(1.5)    # 2700
video.frame_to_minutes(1800)   # 1.0
video.milliseconds_to_frame(500) # 15
video.frame_to_milliseconds(90)  # 3000
```

### `seconds_to_frame(time: float) -> int`
Returns the frame index that corresponds to a specific time in seconds.

### `minutes_to_frame(time: float) -> int`
Returns the frame index that corresponds to a specific time in minutes.

### `milliseconds_to_frame(time: int) -> int`
Returns the frame index that corresponds to a specific time in milliseconds.

### `frame_to_milliseconds(frame: int) -> int`
Returns the time in milliseconds that the given frame will begin.

### `frame_to_seconds(frame: int) -> float`
Returns the time in seconds that the given frame will begin.

### `frame_to_minutes(frame: int) -> float`
Returns the time in minutes that the given frame will begin.