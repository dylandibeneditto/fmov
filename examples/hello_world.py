from fmov import Video
from PIL import Image, ImageDraw

with Video((1920, 1080), framerate=120, path="./video.mp4", prompt_deletion=False) as video:
    for i in range(video.seconds_to_frame(30)):
        img = Image.new("RGB", (video.width, video.height), "#000000")
        draw = ImageDraw.Draw(img)

        #          x    y                 content of the text                     color
        draw.text((100, video.height//2), f"Hello world! This is frame {str(i)}", fill="#ffffff")

        video.pipe(img)

    video.sound_at_frame(frame=10, path="./tests/audio.wav", volume=0.5)

    video.sound_at_millisecond(time=4000, path="./tests/audio.wav", volume=1.0)

    video.sound_at_second(time=25, path="./tests/audio.wav")

