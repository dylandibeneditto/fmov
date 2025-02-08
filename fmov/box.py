from .text import Text

class Box:
    def __init__(
        self,
        position: tuple[int, int],
        background: str,
        width: int = 0,
        height: int = 0,
        corner_radius: float = 0,
        corners: tuple[bool, bool, bool, bool] = (True, True, True, True),
        anchor: str = "topleading",
        opacity: float = 1,
        outline_fill: str = "#000000",
        outline_width: int = 0,
        # TODO: add drop shadow
        content: tuple[(Text | None), (int | tuple[int, int, int, int])] = (None, 0)
    ):
        self.x = position[0]
        self.y = position[1]
        self.w = width
        self.h = height
        self.background = background
        self.corner_radius = corner_radius
        self.corners = corners
        self.anchor = anchor
        self.opacity = opacity
        self.outline_fill = outline_fill
        self.outline_width = outline_width
        self.content = content
        
    def get_width(self):
        width = 0
        if self.content[0] != None:
            if type(self.content[0]) == Text:
                width = self.content[0].get_width()
        else:
            width = self.w
        if type(self.content[1]) == int:
            width += self.content[1] * 2
        elif type(self.content[1]) == tuple[int,int,int,int]:
            width += self.content[1][0] + self.content[1][2]
        return width

    def get_height(self):
        height = 0
        if self.content[0] != None:
            if type(self.content[0]) == Text:
                height = self.content[0].get_height()
        else:
            height = self.h
        if type(self.content[1]) == int:
            height += self.content[1] * 2
        elif type(self.content[1]) == tuple[int,int,int,int]:
            height += self.content[1][1] + self.content[1][3]
        return height

    def display_end_pos(self):
        return (self.display_pos()[0]+self.get_width(), self.display_pos()[1]+self.get_height())

    def display_pos(self):
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

    def display_bg(self):
        return self.background

    def content_pos(self):
        if self.content[0] == None:
            return None

        dp = self.display_pos()
        cdp = self.content[0].display_pos()
        lpad,tpad = (0,0)
        if type(self.content[1]) == int:
            lpad,tpad = (self.content[1], self.content[1])
        elif type(self.content[1]) == tuple[int,int,int,int]:
            lpad = self.content[1][0]
            tpad = self.content[1][1]

        return (dp[0]+lpad+cdp[0], dp[1]+tpad+cdp[1])
