from fmov import Video, Frame, Text, Box

video = Video((1920,1080), framerate=30, path="./video2.mp4")

for i in range(video.seconds_to_frame(30)):
    # background can either be hex or path to an image
    frame = Frame(background="#000000", dimensions=(video.width, video.height), colorspace="RGB")

    # anchor will be one of the following:
    # topleading    top    toptrailing
    # leading       center trailing
    # bottomleading bottom bottomtrailing

    frame_counter = Text(text=f"|frame: {i}", position=(100,100), path="./Inter-VariableFont_opsz,wght.ttf", size=80, color="#ffffff", max_width=10)
    frame_counter.line_limit = 10
    frame_counter.break_line = "letter"
    frame_box = Box(position=(100,100), width=100, height=100, corner_radius=8.0, background="#ff0000")
    frame.add(frame_box)
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

video.render(prompt_deletion=False)
