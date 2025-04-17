# Conversions

Conversions can be helpful when you need to find how many frames are in a certain time frame and vice-versa.

```py title="example"
video = Video(framerate=30)

video.seconds_to_frame(2) # 60
video.frame_to_seconds(60) # 2
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