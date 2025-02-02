from PIL import Image, ImageDraw
from fmov.text import Text
# frame = Frame(background="#000000", dimensions=(video.width, video.height), colorspace="RGB")

class Frame:
    def __init__(
        self,
        dimensions: tuple[int, int] = (0,0),
        background: str = "#000000",
        colorspace: str = "RGB"
    ):
        self.width = dimensions[0]
        self.height = dimensions[1]
        self.background = background
        self.colorspace = colorspace
        self.image = Image.new(colorspace, dimensions, background)
        self.theme = {}

    def add(self, item: (Text | int)):
        draw = ImageDraw.Draw(self.image)
        if type(item) == Text:
            draw.text(item.display_pos(), item.display_text(), font=item.get_font(), fill=item.color)

