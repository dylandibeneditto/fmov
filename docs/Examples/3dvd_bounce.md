# DVD Bounce Example

![output](../assets/dvd.mp4)

```py title="main.py"
from PIL import Image
import random
from fmov import Video
from tqdm import tqdm

with Video(path="./video.mp4", width=1920, height=1080, fps=30) as video:
    # position and velocity of the dvd logo
    x,y = (0,0)
    v = 180//video.fps
    vx, vy = (v,v)

    total_frames = video.time_to_frame("1m")
    
    # using rich.track to keep track of the progress, does a good job of predicting ETA usually
    # keep in mind that this only counts the loading of the video, the audio comes afterward but
    # usually is negligable unless you have a large file with many effects
    for i in tqdm(range(total_frames), total=total_frames, "Rendering..."):
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
            video.sound(path="./audio.wav", at=i)
            hue = (hue+random.randint(20,60))%255

        # position updates
        x += vx
        y += vy

        # finally, append the frame to the end of the video
        video.add(image)
```
