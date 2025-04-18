from PIL import Image, ImageDraw
import random
from rich.progress import track
from fmov import Video

with Video((1920,1080), framerate=30, path="./video.mp4", prompt_deletion=False) as video:
    # position and velocity of the dvd logo
    x,y = (0,0)
    v = 180//video.framerate
    vx, vy = (v,v)

    # create dvd image as a PIL image
    dvd_img = Image.open("./dvd-logo.png")

    # calculation for the new size of the dvd logo while preserving aspect ratio
    img_height = 150
    aspect_ratio = dvd_img.width / dvd_img.height
    img_width = int(img_height * aspect_ratio)
    dvd_img = dvd_img.resize((img_width, img_height))

    # the hue shift value of the dvd logo
    hue = 0

    # the frame index 1 minutes into the video
    # could also be found with...
    # video.milliseconds_to_frame(60000)
    # vidoe.seconds_to_frame(60)
    total_frames = video.minutes_to_frame(1)
    
    # using rich.track to keep track of the progress, does a good job of predicting ETA usually
    # keep in mind that this only counts the loading of the video, the audio comes afterward but
    # usually is negligable unless you have a large file with many effects
    for i in track(range(total_frames), "Rendering...", total=total_frames):
        # initializing the common PIL variables
        image = Image.new("RGB", (video.width, video.height), "#000000")
        #draw = ImageDraw.Draw(image) # usually you need this to draw shapes and text, however this example doesnt require it

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

        # play a sound effect and shift the hue of the logo on a bump
        if bumped:
            video.sound_at_frame(frame=i, path="./audio.wav")
            hue = (hue+random.randint(20,60))%255

        # position updates
        x += vx
        y += vy

        # finally, append the frame to the end of the video
        video.pipe(image)