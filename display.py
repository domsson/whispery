class Display():

    # Return display width in pixels
    def get_width(self):
        raise NotImplementedError((self.__class__.__name__) + "get_width()")

    # Return display height in pixels
    def get_height(self):
        raise NotImplementedError((self.__class__.__name__) + "get_height()")

    # Return the number of characters that
    # can be displayed in one line
    def get_num_chars_per_line(self):
        raise NotImplementedError((self.__class__.__name__) + "get_chars_per_line()")

    # Return the number of lines
    def get_num_lines(self):
        raise NotImplementedError((self.__class__.__name__) + "get_num_lines()")

    # Render the given string in the given line
    # String should only contain ASCII and should
    # not exceed get_num_chars_per_line() length
    def draw_string(self, line, text, align=None):
        raise NotImplementedError((self.__class__.__name__) + "draw_string()")

    # Render the given char in the given line/pos
    def draw_char(self, line, pos, char):
        raise NotImplementedError((self.__class__.__name__) + "draw_char()")

    def clear(self):
        raise NotImplementedError((self.__class__.__name__) + "clear()")

    def display(self):
        raise NotImplementedError((self.__class__.__name__) + "display()")

    def cleanup(self):
        raise NotImplementedError((self.__class__.__name__) + "cleanup()")
