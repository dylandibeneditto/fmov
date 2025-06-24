# Simple Example

![output](../assets/simple.mp4)

```py title="main.py"
from fmov import Video
from PIL import Image, ImageDraw

def generate_frame(frame: int, video: Video) -> Image:
    img = Image.new("RGB", (video.width, video.height), "#000000") #(1)
    draw = ImageDraw.Draw(img) #(2)
    draw.text((100, video.height//2), f"Hello world! This is frame {str(frame)}", fill="#ffffff") #(3)
    return img #(4)

video = Video(path="./video.mp4", dimensions=(1920//2, 1080//2), fps=120, function=generate_frame, length="30s") #(5)
video.preview() #(6)
video.save() #(7)
```

1. This creates the base image for each frame, matching the video size and with a black background.
2. This creates the draw context, allowing you to draw shapes, text, etc.
3. This draws the text on the image, showing the frame number.
4. The frame function returns the image for the current frame.
5. The `Video` object is created with the frame function and length specified. No context manager is needed.
6. `video.preview()` allows you to interactively scrub through the video before rendering.
7. `video.save()` renders the video to the output path.

!!! note Note
    For more about how to create frames with PIL, visit the [PIL documentation](https://pillow.readthedocs.io/en/stable/)