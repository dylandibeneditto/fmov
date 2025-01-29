import fmov
from PIL import Image, ImageDraw
import random
from rich.progress import track

# initialize the video
video = fmov.Video((1920,1080), framerate=30, path="./video.mp4")

# position and velocity of the dvd logo
x,y = (0,0)
v = 180//video.framerate
vx, vy = (v,v)

# create dvd image as a PIL image
dvd_img = Image.open("./tests/dvd-logo.png")

# values to resize the dvd image for the video
img_height = 150
aspect_ratio = dvd_img.width / dvd_img.height
img_width = int(img_height * aspect_ratio)
dvd_img = dvd_img.resize((img_width, img_height))

# the hue shift value of the dvd logo
hue = 0

# the frame index 4 minutes into the video
total_frames = video.minutes_to_frame(5)

for i in track(range(total_frames), "Rendering...", total=total_frames):
    # initializing PIL variables
    image = Image.new("RGB", (video.width, video.height), "#000000")
    draw = ImageDraw.Draw(image)

    # adding the dvd image
    # finding the fill color based on the hue, turn it into an image, and use the dvd image as a mask
    fill_color = Image.new("HSV", (1, 1), (hue, 200, 220)).convert("RGB").getpixel((0, 0))
    color_layer = Image.new("RGB", dvd_img.size, fill_color)
    image.paste(color_layer, (x, y), dvd_img.convert("L") if dvd_img.mode != "RGBA" else dvd_img.split()[3])

    # collision detection
    bumped = False
    if x+vx >= video.width-img_width or x+vx <= 0:
        vx *= -1
        bumped = True
    if y+vy >= video.height-img_height or y+vy <= 0:
        vy *= -1
        bumped = True

    if bumped:
        hue = (hue+random.randint(20,60))%255

    # position updates
    x += vx
    y += vy

    #video.sound_at_frame(frame=i, path="./mysound.wav")
    # append the frame to the video
    video.pipe(image)

#video.sound_at_time(time=1000, path="./mysound.wav")

# render the video 🥳
video.render()
