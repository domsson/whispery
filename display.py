class Display():

    # Return display width in pixels
    def get_width(self):
        raise NotImplementedError("get_width()")

    # Return display height in pixels
    def get_height(self):
        raise NotImplementedError("get_height()")

    # Return the number of characters that
    # can be displayed in one line
    def get_num_chars_per_line(self):
        raise NotImplementedError("get_chars_per_line()")

    # Return the number of lines
    def get_num_lines(self):
        raise NotImplementedError("get_num_lines()")

    # Render the given string in the given line
    # String should only contain ASCII and should
    # not exceed get_num_chars_per_line() length
    def display_string(self, line, text, align=None):
        raise NotImplementedError("display_string()")

    # Render the given char in the given line/pos
    def display_char(self, line, pos, char):
        raise NotImplementedError("display_char()")

    # Renders the given volume [0..100]
    # wherever the implementation sees fit
    def display_volume(self, volume):
        raise NotImplementedError("display_volume()")

    # Renders the given position (in seconds)
    # within an audio file wherever the 
    # implementation sees fit
    def display_position(self, position):
        raise NotImplementedError("display_position()")
