from PIL import Image
import random
from fmov import Video

with Video((1920,1080), fps=30, path="./video.mp4", prompt_deletion=False) as video:
    # position and velocity of the dvd logo
    x,y = (0,0)
    v = 180//video.fps
    vx, vy = (v,v)

def generate_frame(frame: int, video: Video) -> Image:
    global x, y, vx, vy, hue, dvd_img, img_width, img_height
    image = Image.new("RGB", (video.width, video.height), "#000000")
    fill_color = Image.new("HSV", (1, 1), (hue, 200, 220)).convert("RGB").getpixel((0, 0))
    color_layer = Image.new("RGB", dvd_img.size, fill_color)
    image.paste(color_layer, (x, y), dvd_img.convert("L") if dvd_img.mode != "RGBA" else dvd_img.split()[3])
    bumped = False
    # Bounce on X edges
    if x + vx > video.width - img_width or x + vx < 0:
        vx *= -1
        bumped = True
    # Bounce on Y edges
    if y + vy > video.height - img_height or y + vy < 0:
        vy *= -1
        bumped = True
    if bumped:
        video.audio("./audio.wav", at=frame)
        hue = (hue + random.randint(20, 60)) % 255
    x += vx
    y += vy
    return image

video = Video(path="output.mp4", dimensions=(1920, 1080), fps=30, function=generate_frame, length="10s")
video.preview()
video.save()