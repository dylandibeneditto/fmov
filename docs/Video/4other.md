# Miscellaneous Utilities

### `set_path(path: str) -> None`
Updates the output path for the video file. Useful if you want to change the output location after creating the `Video` object.

```py title="example"
video = Video(path="./original.mp4")
video.set_path("./new_output.mp4")
```

### `get_path() -> str`
Returns the current output path for the video file.

```py title="example"
current_path = video.get_path()
```