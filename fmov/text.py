from PIL import ImageFont, Image, ImageDraw
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
                 anchor: str = "topleading",
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

    def get_lines(self):
        text = self.display_text()
        result = 1
        while "\n" in text:
            text = text.replace("\n","")
            result += 1
        return result

    def get_str_size(self, s: str) -> tuple[float, float]:
        draw = ImageDraw.Draw(Image.new("RGBA", (0,0), (255, 255, 255, 0)))

        font = self.get_font()

        descent = 0
        if type(font) != ImageFont.ImageFont:
            descent = font.getmetrics()[1]

        text_width, text_height = draw.textbbox((0, 0), s, font=font)[2:4]
        return (text_width, text_height+descent)

    def get_size(self) -> tuple[float, float]:
        return self.get_str_size(self.display_text())

    def get_font(self) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
        if self.path != "":
            if os.path.exists(self.path):
                return ImageFont.truetype(self.path, self.size)
            else:
                raise FileNotFoundError(f"Cannot find text file {self.path}")
        else:
            return ImageFont.load_default(size=self.size)

    def display_pos(self) -> tuple[int, int]:
        x, y = (self.x, self.y)

        if "top" in self.anchor:
            pass
        elif "bottom" in self.anchor:
            y -= int(self.get_size()[1])
        else:
            y -= self.get_size()[1] // 2

        if "leading" in self.anchor:
            pass
        elif "trailing" in self.anchor:
            x -= int(self.get_size()[0])
        else:
            x -= self.get_size()[0] // 2

        return (int(x), int(y))

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
            word_width = self.get_str_size(line)[0]

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
