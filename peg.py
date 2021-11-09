from color import color_text

class Peg:
    def __init__(self, color, icon="✱"):
        self.color = color
        self.icon = icon
    def get_text(self):
        """Returns colored icon text representation of peg"""
        return color_text(*self.color.rgb, self.icon)