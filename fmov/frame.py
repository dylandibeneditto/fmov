from PIL import Image, ImageDraw
from fmov.text import Text
from fmov.box import Box
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

    def __insert(self, item, position):
        draw = ImageDraw.Draw(self.image)
        if type(item) == Text:
            draw.text(position, item.display_text(), font=item.get_font(), fill=item.color)
        if type(item) == Box:
            draw.rounded_rectangle((*position,*item.display_end_pos()), radius=item.corner_radius, fill=item.display_bg(), outline=item.outline_fill, width=item.outline_width, corners=item.corners)

    def add(self, item: (Text | Box)):
        self.__insert(item, item.display_pos())
        if type(item) == Box:
            if item.content[0] != None:
                self.__insert(item.content[0], item.content_pos())
