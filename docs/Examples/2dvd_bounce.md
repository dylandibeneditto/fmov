# DVD Bounce Example

![output](../assets/dvd.mp4)

```py title="main.py"
from PIL import Image
import random
from fmov import Video

with Video(path="./video.mp4", (1920,1080), fps=30) as video:
    # position and velocity of the dvd logo
    x,y = (0,0)
    v = 180//video.fps
    vx, vy = (v,v)

def generate_frame(frame: int, video: Video) -> Image:
    global x, y, vx, vy, hue, dvd_img, img_width, img_height
    image = Image.new("RGB", (video.width, video.height), "#000000")  # (11)
    fill_color = Image.new("HSV", (1, 1), (hue, 200, 220)).convert("RGB").getpixel((0, 0))  # (12)
    color_layer = Image.new("RGB", dvd_img.size, fill_color)  # (13)
    image.paste(color_layer, (x, y), dvd_img.convert("L") if dvd_img.mode != "RGBA" else dvd_img.split()[3])  # (14)
    bumped = False
    if x + vx > video.width - img_width or x + vx < 0:
        vx *= -1
        bumped = True
    if y + vy > video.height - img_height or y + vy < 0:
        vy *= -1
        bumped = True
    if bumped:
        video.audio("./audio.wav", at=frame)  # (15)
        hue = (hue + random.randint(20, 60)) % 255  # (16)
    x += vx  # (17)
    y += vy  # (18)
    return image  # (19)

video = Video(path="output.mp4", dimensions=(1920, 1080), fps=30, function=generate_frame, length="1m")  # (20)
video.preview()  # (21)
video.save()  # (22)
```

1. Initial x position of the logo
2. Initial y position of the logo
3. Initial x velocity
4. Initial y velocity
5. Initial hue for color shifting
6. Load the DVD logo image
7. Set the height for the logo
8. Calculate the aspect ratio
9. Calculate the width for the logo
10. Resize the logo to the correct size
11. Create the base image for each frame
12. Calculate the fill color based on the hue
13. Create a color layer for the logo
14. Paste the colored logo onto the frame
15. Play a sound when the logo bounces
16. Change the hue on bounce
17. Update x position
18. Update y position
19. Return the frame image
20. Create the Video object with the frame function and length
21. Preview the video interactively
22. Render the video to the output path

    total_frames = video.time_to_frame("1m")
    
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
            video.sound(path="./audio.wav", at=i)
            hue = (hue+random.randint(20,60))%255

        # position updates
        x += vx
        y += vy

        # finally, append the frame to the end of the video
        video.pipe(image)
```
