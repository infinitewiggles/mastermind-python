class Color:
    def __init__(self, *args):
        if len(args) == 3:
            self.rgb = self._rgb(args)
        elif len(args) == 1:
            item = args[0]
            if type(item) == tuple:
                self.rgb = self._rgb(item)
            elif type(item) == str:
                self.rgb = self._hex(item)
            else:
                raise ValueError("Unsupported color argument(s)")
        else:
            raise ValueError("Unsupported color argument(s)")
                
    def _rgb(self, values):
        """Converts supplied value into RGB and checks that it's a valid input"""
        check = range(0, 256)
        for value in values:
            if int(value) not in check: raise ValueError(f"{value} RGB value not within range (0-255)")
        return tuple(values)
        
    def _hex(self, value):
        """Converts supplied value into RGB and checks that it's a valid input"""
        corrected = None
        if len(value) == 7:
            corrected = value[1:]
        elif len(value) == 6:
            corrected = value
        else:
            raise ValueError(f"Invalid hexidecimal argument: {value}")
        
        return (int(corrected[0:2], base=16), int(corrected[2:4], base=16), int(corrected[4:6], base=16))

    def equals(self, another_color):
        """Checks self rgb value against another color to determine if the colors are the same"""
        return self.rgb == another_color.rgb
        
def color_text(r, g, b, text):
    """Turns an RGB value into an ANSI color, then adds the ANSI escape code and returns the coloured text,
    basic functionality taken from: https://stackoverflow.com/a/26665998
    """
    ansi = 0

    if r is g and g is b:
        if r < 8:
            ansi = 16;
        elif r > 248:
            ansi = 231;
        else:
            ansi = int((r - 8) / 247 * 24) + 232;
    else:
        ansi = 16 + 36 * int(r / 255 * 5) + 6 * int(g / 255 * 5) + int(b / 255 * 5);

    return "\033[38;5;" + str(ansi) + "m" + text + "\033[0;00m"