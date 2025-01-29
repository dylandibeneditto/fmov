import fmov
from PIL import Image, ImageDraw

# create video with pipe
video = fmov.Video((1920,1080), framerate=60, path="./video.mp4", vcodec="libx264", pix_fmt="yuv420p", render_preset="ultrafast", crf=8, audio_bitrate="192k")

x,y = (0,0)
vx, vy = (2,2)
for i in range(60*60):

    image = Image.new("RGB", (1920, 1080), "#ffffff")
    draw = ImageDraw.Draw(image)

    draw.rectangle((x,y,x+50,y+50), fill="#000000")

    if x+vx >= 1920-50 or x+vx <= 0:
        vx *= -1
    if y+vy >= 1080-50 or y+vy <= 0:
        vy *= -1

    x += vx
    y += vy

    #video.sound_at_frame(frame=i, path="./mysound.wav")
    video.pipe(image)

#video.sound_at_time(time=1000, path="./mysound.wav")

video.render()

# create video through collecting frames from disk
#video = fmov.Video((1920,1080), framerate=30, path="./video.mp4", vcodec="libx264", pix_fmt="yuv420p", render_preset="ultrafast", crf=8, audio_bitrate="192k")

#video.from_images(path="./out/*.png")

#video.save()
