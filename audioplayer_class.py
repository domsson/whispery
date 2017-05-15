class AudioPlayer():

    # Add a given file to the list of files
    # Returns the new number of files in the file list
    def add(self, mrl):
        raise NotImplementedError((self.__class__.__name__) + ".add()")

    # Add the given files to the list of files
    # Returns the new number of files in the file list
    def add_all(self, mrl):
        raise NotImplementedError((self.__class__.__name__) + ".add_all()")

    # Load a given file and free all previously loaded files
    # Return 1 on success, 0 on failure
    def load(self, mrl):
        raise NotImplementedError((self.__class__.__name__) + ".load()")

    # Load a given list of files and free all previously loaded files
    # Return the number of files loaded
    def load_all(self, mrls):
        raise NotImplementedError((self.__class__.__name__) + ".load_all()")

    # Return the number of loaded files
    def num_files(self):
        raise NotImplementedError((self.__class__.__name__) + ".num_files()")
    
    # Return the file name of the current or specified file (by index)
    def get_filename(self, index=-1):
        raise NotImplementedError((self.__class__.__name__) + ".get_filename()")

    # Return the name of the current or specified file's artist
    # This should be the author. If not set, return `None`
    def get_author(self, index=-1):
        raise NotImplementedError((self.__class__.__name__) + ".get_author()")

    # Return the name of the current of specified file's title
    # This should be the title of the book. If not set, return `None`
    def get_title(self, index=-1):
        raise NotImplementedError((self.__class__.__name__) + ".get_title()")

    # Return the length (in seconds) of the current or specified file
    def get_duration(self, index=-1):
        raise NotImplementedError((self.__class__.__name__) + ".get_duration()")
    
    # Return the index of the current file
    def get_current(self):
        raise NotImplementedError((self.__class__.__name__) + ".get_current()")

    # Return the current volume [0..100]
    def get_volume(self):
        raise NotImplementedError((self.__class__.__name__) + ".get_volume()")

    # Set the volume to the specified value [0..100]
    # Return the new set volume
    def set_volume(self, volume):
        raise NotImplementedError((self.__class__.__name__) + ".set_volume()")

    # Return the current position within the file, in seconds
    def get_position(self):
        raise NotImplementedError((self.__class__.__name__) + ".get_position()")

    # Seek to the specified position, in seconds
    # Return the new position
    def set_positon(self, position):
        raise NotImplementedError((self.__class__.__name__) + ".set_position()")

    # Change posiiton relative from the current one, in seconds
    # Return the new position
    def seek(self, seconds):
        raise NotImplementedError((self.__class__.__name__) + ".seek()")

    # Go to the beginning of the previous file (if multiple loaded)
    # Return the numberof the new file or -1 if there is no previous.
    def prev():
        raise NotImplementedError((self.__class__.__name__) + ".prev()")

    # Go to the beginning of the next file (if multiple loaded)
    # Return the number of the new file or -1 if there is no next.
    def next():
        raise NotImplementedError((self.__class__.__name__) + ".next()")

    # Start/Resume the playback from the current position
    def play():
        raise NotImplementedError((self.__class__.__name__) + ".play()")

    # Pause the playback and remember the current position
    def pause():
        raise NotImplementedError((self.__class__.__name__) + ".pause()")

    # Play or pause playback depening on current playback status
    def toggle_playback():
        raise NotImplementedError((self.__class__.__name__) + ".toggle_playback()")

    # Return `True` if currently playing, otherwise `False`
    def is_playing(self):
        raise NotImplementedError((self.__class__.__name__) + ".is_playing()")

    # Halt playback and set position to 0
    def stop(self):
        raise NotImplementedError((self.__class__.__name__) + ".stop()")

    # Halt playback, free all resources, clean up after yourself
    def cleanup(self):
        raise NotImplementedError((self.__class__.__name__) + ".cleanup()")
