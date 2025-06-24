from fmov import Video
from PIL import Image, ImageDraw
import numpy as np

def generate_frame(frame: int, video: Video) -> Image:
    img = Image.new("RGB", (video.width, video.height), "#000000")
    draw = ImageDraw.Draw(img)
    draw.text((100, video.height//2), f"Hello world! This is frame {str(frame)}", fill="#ffffff")
    return img

video = Video(path="output.mp4", dimensions=(1920//2, 1080//2), fps=120, function=generate_frame, length="30s")
video.preview()
video.save()

