from fmov import Video
from PIL import Image, ImageDraw
import numpy as np

with Video("video.mp4", (1920//2, 1080//2), fps=120) as video:
    for i in range(video.seconds_to_frame(30)):
        img = Image.new("RGB", (video.width, video.height), "#000000")
        draw = ImageDraw.Draw(img)

        #          x    y                 content of the text                     color
        draw.text((100, video.height//2), f"Hello world! This is frame {str(i)}", fill="#ffffff")

        video.pipe(img)

    video.sound(path="./audio.wav", at="100", volume=0.5)

    video.sound(path="./audio.wav", at="4000ms")

    video.sound(path="./audio.wav", at="25s 500ms")
