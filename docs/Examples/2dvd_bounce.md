# DVD Bounce Example

![output](../assets/dvd.mp4)

```py title="main.py"
from PIL import Image
import random
from fmov import Video

x = 0  # (1)
y = 0  # (2)
vx = 8  # (3)
vy = 8  # (4)
hue = 0  # (5)
dvd_img = Image.open("./dvd-logo.png")  # (6)
img_height = 150  # (7)
aspect_ratio = dvd_img.width / dvd_img.height  # (8)
img_width = int(img_height * aspect_ratio)  # (9)
dvd_img = dvd_img.resize((img_width, img_height))  # (10)

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

- The DVD logo bounces off the edges of the screen, changing color and playing a sound each time it hits a wall.
- All state is managed with global variables for clarity.
- The frame function returns the image for the current frame.
- `video.audio()` is called on each bounce to register a sound event.
- `video.preview()` allows you to scrub and debug before rendering.
- `video.save()` renders the video to the output path.