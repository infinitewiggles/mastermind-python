import color, peg
from color import color_text

class Row:
    def __init__(self):
        blank_peg = peg.Peg(color.Color(255, 255, 255))
        self.row = [blank_peg for _ in range(4)]
        self.prefix = ""
        self.suffix = " "
    def set_peg(self, index, peg):
        """Sets peg object at index"""
        self.row[index] = peg
    def get_peg(self, index):
        """Returns peg object at index"""
        return self.row[index]
    def get_text(self):
        """Gets text representation of row"""
        return self.prefix + " ".join([peg.get_text() for peg in self.row]) + self.suffix
    def mark(self, green, orange):
        """Adds mark to end of row text"""
        self.suffix = " " + color_text(0, 255, 0, str(green)) + " " + color_text(255, 165, 0, str(orange))