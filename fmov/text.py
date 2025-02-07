from PIL import ImageFont
import os

# frame_counter = Text(text=f"frame: {i}", font_path="./something.ttf", size=18, position=(1920//2, 1080//2), color="#ffffff", opacity=0.4, anchor="center", max_width=200, break_line="word", line_limit=2)
    
class Text:
    def __init__(self,
                 text: str,
                 position: tuple[int, int] = (0,0),
                 path: str = "",
                 size: int = 18,
                 color: str = "#000000",
                 opacity: float = 1.0,
                 anchor: str = "leading",
                 max_width: int = 0,
                 break_line: str = "word",
                 line_limit: int = 1,
                 truncate_with_ellipsis: bool = True
        ):
        self.text = text
        self.path = path
        self.size = size
        self.x = position[0]
        self.y = position[1]
        self.color = color
        self.opacity = opacity
        self.anchor = anchor
        self.max_width = max_width
        self.break_line = break_line
        self.line_limit = line_limit
        self.truncate_with_ellipsis = truncate_with_ellipsis

    def get_metrics(self):
        font = self.get_font()
        if type(font) == ImageFont.FreeTypeFont:
            return font.getmetrics()
        else:
            return (0,0)

    def get_str_width(self, s: str) -> float:
        return max(self.get_font().getlength(i) for i in s.split("\n"))

    def get_str_height(self, s: str) -> float:
        # TODO: fix the issue with y position being incorrect
        ascent, descent = self.get_metrics()
        height = self.get_font().getmask(s).getbbox()[3]
        descent_height = height + descent
        return height - descent + ascent

    def get_width(self) -> float:
        return self.get_str_width(self.display_text())

    def get_height(self) -> float:
        return self.get_str_height(self.display_text())

    def get_font(self) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
        if self.path != "":
            if os.path.exists(self.path):
                return ImageFont.truetype(self.path, self.size)
            else:
                raise FileNotFoundError(f"Cannot find text file {self.path}")
        else:
            return ImageFont.load_default(size=self.size)

    def display_pos(self) -> tuple[int, int]:
        x,y = (self.x, self.y+self.get_metrics()[1])

        if "top" in self.anchor:
            pass
        elif "bottom" in self.anchor:
            y -= int(self.get_height())
        else:
            y -= self.get_height()//2

        if "leading" in self.anchor:
            pass
        elif "trailing" in self.anchor:
            x -= int(self.get_width())
        else:
            x -= self.get_width()//2

        return (int(x),int(y))

    def display_text(self) -> str:
        if self.max_width == 0:
            return self.text

        replace = " " if self.break_line=="word" else ""
        words = self.text.split(" ") if self.break_line == "word" else list(self.text)
        result = ""
        line = ""
        current_x = 0
        line_count = 0

        for word in words:
            line = word + replace
            word_width = self.get_str_width(line)

            if current_x + word_width > self.max_width:
                if line_count == self.line_limit:
                    if self.truncate_with_ellipsis:
                        result = result.rstrip()[:-3] + "..."
                    break
                result += "\n"
                current_x = 0
                line_count += 1

            current_x += word_width
            result += line

        return result
