import fmov

video = Video((1920,1080), framerate=30, path="./video2.mp4")

for i in range(video.seconds_to_frame(30)):
    # background can either be hex or path to an image
    frame = Frame(background="#000000", (video.width, video.height), colorspace="RGB")

    # anchor will be one of the following:
    # topleading    top    toptrailing
    # leading       center trailing
    # bottomleading bottom bottomtrailing

    # truncation mode will be one of the following:
    # letter    word    punctuation
    frame_counter = Text(text=f"frame: {i}", font_path="./something.ttf", size=18, position=(1920//2, 1080//2), color="#ffffff", anchor="center", max_width=200, truncation_mode="word", line_limit=2)
    frame_counter.truncation_mode = "letter"
    frame_counter.truncate_with_ellipses = False
    frame.add(frame_counter)

    # put in None for values in the size where it will be automatically found
    # (100, None) resizes to 100 pixels wide
    # (None, 100) resizes to 100 pixels tall
    # (None, None) wont resize the image
    logo = Image(path="./logo.png", position=(10,10), size=(100, None), transparent=True)
