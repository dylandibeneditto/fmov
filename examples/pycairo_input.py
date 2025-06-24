import cairo
import numpy as np
from PIL import Image
from fmov import Video

def pilImageFromCairoSurface(surface):
    cairoFormat = surface.get_format()
    if cairoFormat == cairo.FORMAT_ARGB32:
        pilMode = 'RGB'
        argbArray = np.frombuffer(surface.get_data(), dtype=np.uint8).reshape(-1, 4)
        rgbArray = argbArray[:, 2::-1]
        pilData = rgbArray.reshape(-1).tobytes()
    else:
        raise ValueError('Unsupported cairo format: %d' % cairoFormat)
    pilImage = Image.frombuffer(pilMode,
        (surface.get_width(), surface.get_height()), pilData, "raw",
        pilMode, 0, 1)
    pilImage = pilImage.convert('RGB')
    return pilImage

def generate_frame(frame: int, video: Video) -> Image:
    width, height = video.width, video.height
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    ctx = cairo.Context(surface)
    ctx.set_source_rgba(0, 0, 0, 0)
    ctx.paint()
    ctx.set_source_rgba(1.0, 0.0, 0.0, 0.5)
    x_position = 50 + (frame * 5) % (width - 300)
    ctx.rectangle(x_position, 50, 300, 200)
    ctx.fill()
    return pilImageFromCairoSurface(surface)

video = Video(path="output.mp4", dimensions=(1920, 1080), fps=30, function=generate_frame, length="10s")
video.preview()
video.save()