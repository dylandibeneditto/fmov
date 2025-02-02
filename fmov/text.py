from PIL import ImageFont
import os

# frame_counter = Text(text=f"frame: {i}", font_path="./something.ttf", size=18, position=(1920//2, 1080//2), color="#ffffff", opacity=0.4, anchor="center", max_width=200, break_line="word", line_limit=2)
    
class Text:
    def __init__(self,
                 text: str,
                 position: tuple[int, int],
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

    def get_str_width(self, s: str) -> float:
        return self.get_font().getmask(s).getbbox()[2]
    def get_str_height(self, s: str) -> float:
        descent = 0
        # font = self.get_font()
        # if type(font) != ImageFont.ImageFont:
            # descent = font.getmetrics()[1]
        return self.get_font().getmask(s).getbbox()[3] + descent
    def get_width(self) -> float:
        return self.get_str_width(max(self.display_text().split('\n')))

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
        x,y = (self.x, self.y)

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

        split_indices = []
        splitter = " "

        result = ""

        if self.break_line == "letters":
            splitter = ""
        elif self.break_line == "punctuation":
            splitter = ",|;|.|!|?|:"

        for (n, i) in enumerate(self.text):
            delimiters = splitter.split("|")
            for j in delimiters:
                if i == j:
                    split_indices.append(n+1)

        line_count = 0
        current_x = 0
        for (n, i) in enumerate(split_indices):
            substr = self.text[(split_indices[n-1] if n != 0 else 0):i]
            substr_width = self.get_str_width(substr)

            if current_x + substr_width > self.max_width:
                if line_count == self.line_limit:
                    if self.truncate_with_ellipsis:
                        result = result[:-3]+"..."
                    break
                substr = f"\n{substr}"

            result += substr
            current_x += substr_width

            if '\n' in substr:
                current_x = 0
                line_count += 1

        return result
