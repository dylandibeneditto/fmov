from PIL import Image
import random
from fmov import Video

def generate_frame(frame: int, video: Video) -> Image:
    if not hasattr(generate_frame, 'x'):
        generate_frame.x = 0
        generate_frame.y = 0
        generate_frame.vx = 180 // video.fps
        generate_frame.vy = 180 // video.fps
        generate_frame.hue = 0
        generate_frame.dvd_img = Image.open("./examples/dvd\ bounce/dvd-logo.png")
        img_height = 150
        aspect_ratio = generate_frame.dvd_img.width / generate_frame.dvd_img.height
        img_width = int(img_height * aspect_ratio)
        generate_frame.dvd_img = generate_frame.dvd_img.resize((img_width, img_height))
        generate_frame.img_width = img_width
        generate_frame.img_height = img_height
    x, y = generate_frame.x, generate_frame.y
    vx, vy = generate_frame.vx, generate_frame.vy
    hue = generate_frame.hue
    dvd_img = generate_frame.dvd_img
    img_width = generate_frame.img_width
    img_height = generate_frame.img_height
    image = Image.new("RGB", (video.width, video.height), "#000000")
    fill_color = Image.new("HSV", (1, 1), (hue, 200, 220)).convert("RGB").getpixel((0, 0))
    color_layer = Image.new("RGB", dvd_img.size, fill_color)
    image.paste(color_layer, (x, y), dvd_img.convert("L") if dvd_img.mode != "RGBA" else dvd_img.split()[3])
    bumped = False
    if x+vx >= video.width-img_width or x+vx <= 0:
        vx *= -1
        bumped = True
    if y+vy >= video.height-img_height or y+vy <= 0:
        vy *= -1
        bumped = True
    if bumped:
        video.audio("./examples/dvd\ bounce/audio.wav", at=frame)
        hue = (hue+random.randint(20,60))%255
    x += vx
    y += vy
    generate_frame.x = x
    generate_frame.y = y
    generate_frame.vx = vx
    generate_frame.vy = vy
    generate_frame.hue = hue
    return image

video = Video(path="output.mp4", dimensions=(1920, 1080), fps=30, function=generate_frame, length="1m")
video.preview()
video.save()