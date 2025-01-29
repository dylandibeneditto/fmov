import fmov
from PIL import Image, ImageDraw

# create video with pipe
video = fmov.Video((1920,1080), framerate=30, path="./video.mp4", vcodec="libx264", pix_fmt="yuv420p", render_preset="ultrafast", crf=8, audio_bitrate="192k")

for i in range(100):

    image = Image.new("RGB", (1920, 1080), "#ffffff")
    draw = ImageDraw.Draw(image)

    draw.text((100+i,100), "hello world", fill="#000000")

    #video.sound_at_frame(frame=i, path="./mysound.wav")
    video.pipe(image)

#video.sound_at_time(time=1000, path="./mysound.wav")

video.render()

# create video through collecting frames from disk
#video = fmov.Video((1920,1080), framerate=30, path="./video.mp4", vcodec="libx264", pix_fmt="yuv420p", render_preset="ultrafast", crf=8, audio_bitrate="192k")

#video.from_images(path="./out/*.png")

#video.save()
