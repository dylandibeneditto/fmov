# Hello World with PIL

![output](../assets/start.mp4)

```py title="main.py"
from fmov import Video
from PIL import Image, ImageDraw
from tqdm import tqdm

# using 'with Video() as video' makes rendering simpler, as when the context ends it calls render automatically
with Video(path="video.mp4", width=1920, height=1080, fps=60) as video:
    total_frames = video.time_to_frame("20s") # turns the timestamp "20s" into the number of frames in the video

    # create all the frames in the video (tqdm is a progress bar)
    for i in tqdm(range(total_frames), total=total_frames, desc="Rendering"):

        # PIL stuff, just rendering out the text "Hello World"
        img = Image.new("RGB", (video.width, video.height), "#000000")
        draw = ImageDraw.Draw(img)

        draw.text(
            (100, video.height // 2),
            f"Hello world! This is frame {i}",
            fill="#ffffff"
        )

        video.add(img) # add the frame to the end of the video
```

If you would like to see how to make a significantly more performant video, see the [OpenCV Example](./2opencv.md)

!!! note Note
    For more about how to create frames with PIL, visit the [PIL documentation](https://pillow.readthedocs.io/en/stable/)
