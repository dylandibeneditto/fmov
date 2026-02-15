# Miscellaneous Utilities

## `set_path(path: str) -> None`
Updates the output path for the video file. Useful if you want to change the output location after creating the `Video` object.

```py title="example"
video = Video(path="./original.mp4")
video.set_path("./new_output.mp4")
```

---

## `get_path() -> str`
Returns the current output path for the video file.

```py title="example"
current_path = video.get_path()
```

---

## `vcodec: dict`
Every video object has a vcodec block. Parameters such as bitrate, compression, and others can be found inside this object.

The contents will be different based on the vcodec selected, although the `name` key value pair will be present for all vcodecs.

!!! warning "The contents of this dictionary may change unless told otherwise"
    vcodec is decided at the creation of the `Video` object, if changes in available codecs occur this could alter the contents of the dictionary, as they are reliant on the vcodec. If it is necessary, manually set your vcodec with `video.set_vcodec`

---

## `set_vcodec(vcodec: str) -> None`
Updates the vcodec manually. See FFmpeg documentation for more on how vcodecs work.


