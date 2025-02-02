from fmov import Video, Frame, Text
from PIL import ImageDraw

video = Video((1920,1080), framerate=30, path="./video2.mp4")

for i in range(video.seconds_to_frame(30)):
    # background can either be hex or path to an image
    frame = Frame(background="#000000", dimensions=(video.width, video.height), colorspace="RGB")

    # anchor will be one of the following:
    # topleading    top    toptrailing
    # leading       center trailing
    # bottomleading bottom bottomtrailing

    # truncation mode will be one of the following:
    # letter    word    punctuation
    frame_counter = Text(text=f"frame: {i} asldkfj alksjf laskjdflaks dflakjsdfalkjsdflasjd flakjsdflkajs fdlkjalsdjf ", path="./Inter-VariableFont_opsz,wght.ttf", size=18, position=(1920//2, 1080//2), color="#ffffff", anchor="center", max_width=200)
    frame_counter.line_limit = 4
    frame_counter.break_line = "letter"
    print(frame_counter.get_str_width("hello"), frame_counter.get_height())
    ImageDraw.Draw(frame.image).rectangle((1920//2-100,1080//2-100,1920//2+100,1080//2+100), fill="#ff0000")
    frame.add(frame_counter)


    # put in None for values in the size where it will be automatically found
    # (100, None) resizes to 100 pixels wide
    # (None, 100) resizes to 100 pixels tall
    # (None, None) wont resize the image
    # logo = Img(path="./logo.png", position=(10,10), size=(100, None), transparent=True)
    # frame.add(logo)

    # image = Image.new("RGB", (video.width,video.height), "#00ff00")
    # image_obj = PILImg(ref=image, position=(0,0))
    # frame.add(image_obj)

    video.pipe(frame.image)

video.render()
