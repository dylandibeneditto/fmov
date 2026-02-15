# Simple Example

![output](../assets/simple.mp4)

```py title="main.py"
from fmov import Video
from PIL import Image, ImageDraw

with Video("video.mp4", (1920//2, 1080//2), fps=120) as video: #(1)
    for i in range(video.seconds_to_frame(30)): #(2)
        img = Image.new("RGB", (video.width, video.height), "#000000") #(3)
        draw = ImageDraw.Draw(img) #(4)

        #          x    y                 content of the text                     color
        draw.text((100, video.height//2), f"Hello world! This is frame {str(i)}", fill="#ffffff")

        video.pipe(img) #(5)

    video.sound(path="./audio.wav", at="100", volume=0.5)

    video.sound(path="./audio.wav", at="4000ms")

    video.sound(path="./audio.wav", at="25s 500ms")
```

1. Creating the video via Context Manager. This video is a 1920 x 1080 video with a fps of 120fps. The video will be saved at './video.mp4'

2. This code loops through every frame that will make up a 30 second video

3. This creates the base image that we will draw on, the image is the same size as the video and will have a background color of black

4. This creates the draw context along with the image, which allows us to draw rectangles, text, etc.

5. This adds the frame to the video

!!! note Note
    For more about how to create frames with PIL, visit the [PIL documentation](https://pillow.readthedocs.io/en/stable/)
