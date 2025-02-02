from typing import Tuple
from PIL import ImageFont
import os

# frame_counter = Text(text=f"frame: {i}", font_path="./something.ttf", size=18, position=(1920//2, 1080//2), color="#ffffff", anchor="center", max_width=200, truncation_mode="word", line_limit=2)
    
class Text:
    def __init__(self, text: str,
                 position: tuple[int, int],
                 path: str = "",
                 size: int = 18,
                 color: str = "#000000",
                 anchor: str = "leading",
                 max_width: int = 0,
                 truncation_mode: str = "word",
                 line_limit: int = 1
                 ):
        self.text = text
        self.path = path
        self.size = size
        self.x = position[0]
        self.y = position[1]
        self.color = color
        self.anchor = anchor
        self.max_width = max_width
        self.truncation_mode = truncation_mode
        self.line_limit = line_limit

    def get_width(self) -> float:
        return min(self.max_width, self.get_font().getbbox(self.__display_text())[0])

    def get_font(self) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
        if self.path:
            if os.path.exists(self.path):
                return ImageFont.truetype(self.path, self.size)
            else:
                raise FileNotFoundError(f"Cannot find text file {self.path}")
        else:
            return ImageFont.load_default(size=self.size)

    def __display_text(self):
        return "blah blah blah"
