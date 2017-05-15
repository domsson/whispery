# Implements the abstract AudioPlayer class
# using VLC via Python's libvlc bindings

import vlc
from audioplayer_class import AudioPlayer

class VLC(AudioPlayer):

    options = [
        "--aout=alsa",
        "--novideo"
    ]

    volume_def = 50
    volume_min = 0
    volume_max = 100

    def __init__(self, volume=None):
        self.instance = vlc.Instance(" ".join(VLC.options))
        self.player = self.instance.media_player_new()
        self.media = []
        self.current = -1
        if volume:
            self.volume_ini = volume
        else:
            self.volume_ini = VLC.volume_def
        self.player.audio_set_volume(self.volume_ini)

    # Halt playback and release all resources, effectively
    # resetting the instance to its initial state
    # However, by default, the set volume will be kept
    def reset(self, reset_volume=False):
        volume = self.get_volume()  # Remember volume (is -1 while stopped!)
        self.stop()                 # Halt playback

        if self.player:
            self.player.release()
            self.player = self.instance.media_player_new()
            if reset_volume:
                self.set_volume(self.volume_ini)
            else:
                self.set_volume(volume)

        for m in self.media:
            m.release()
        
        self.media = []
        self.current = -1

    # Turn the selected file into media to make it the current file
    # This is required in order to play the selected file
    def init_media(self, index):
        if index < 0 or index >= len(self.files):
            raise IndexError((self.__class__.__name__) + ".init_media()")
        self.player.set_media(self.media[index])
        self.current = index

    # Add a given file to the list of files
    # Returns the new number of files in the file list
    def add(self, mrl):
        new_media = self.instance.media_new(mrl)
        self.media.append(new_media)
        self.media[-1].parse() # Start parsing meta data...
        return len(self.media)

    # Add the given files to the list of files
    # Returns the new number of files in the file list
    def add_all(self, mrls):
        for mrl in mrls:
            self.add(mrl)
        return len(self.media)

    # Load a given file. Frees all currently loaded files
    # Return 1 on success, 0 on failure
    def load(self, mrl):
        self.reset()                # Release the current playlist
        num_files = self.add(mrl)   # Add the file to the list of files
        if num_files > 0:
            self.init_media(0)      # Load the first file into the player
            return 1
        return 0

    # Load a given list of files and free all previously loaded files
    # Return the number of files loaded
    def load_all(self, mrls):        
        if len(mrls) == 0:
            return 0

        self.reset()                    # Release the current playlist
        num_files = self.add_all(mrls)  # Add the files to the list of files
        if num_files > 0:
            self.init_media(0)          # Load the first file into the player
        return num_files

    # Return the number of loaded files
    def num_files(self):
        return len(self.media)
    
    # Return the file name of the current or specified file (by index)
    def get_filename(self, index=-1):
        if index == -1:
            index = self.current
        if index < 0 or index >= self.num_files():
            raise IndexError((self.__class__.__name__) + ".get_filename()")

        return self.files[index]

    # Return the name of the current or specified file's artist
    # This should be the author. If not set, return `None`
    def get_author(self, index=-1):
        if index == -1:
            index = self.current
        if index < 0 or index >= self.num_files():
            raise IndexError((self.__class__.__name__) + ".get_author()")

        return self.media[index].get_meta(vlc.Meta.Artist)

    # Return the name of the current of specified file's title
    # This should be the title of the book. If not set, return `None`
    def get_title(self, index=-1):
        if index == -1:
            index = self.current
        if index >= self.num_files():
            raise IndexError((self.__class__.__name__) + ".get_title()")

        album = self.media[index].get_meta(vlc.Meta.Album) 
        title = self.media[index].get_meta(vlc.Meta.Title)

        if album:
            return album
        else:
            return title

    # Return the length (in seconds) of the current or specified file
    def get_duration(self, index=-1):
        if index == -1:
            index = self.current
        if index < 0 or index >= self.num_files():
            raise IndexError((self.__class__.__name__) + ".get_duration()")

        duration = self.media[index].get_duration() # ms, exact
        return duration // 1000 # s, rounded
    
    # Return the index of the current file
    def get_current(self):
        return self.current

    # Return the current volume [0..100]
    def get_volume(self):
        return self.player.audio_get_volume()

    # Set the volume to the specified value [0..100]
    # Return the new volume
    def set_volume(self, volume):
        if volume < 0:
            volume = 0
        elif volume > 100:
            volume = 100
        self.player.audio_set_volume(volume)
        return volume

    # Return the current position within the file, in seconds
    def get_position(self):
        return self.get_duration() * self.get_position_relative()

    # Seek to the specified position, in seconds
    # Return the new position
    def set_positon(self, position):
        pos = position / self.get_position()
        self.set_position_relative(pos)
        return self.get_position()

    # Get relative position (range [0.0..0.1]
    def get_position_relative(self):
        return self.player.get_position() # [0.0..1.0]

    # Set position with a relative value (range [0.0..0.1]
    def set_position_relative(self, pos):
        if pos < 0.0:
            pos = 0.0
        elif pos > 1.0:
            pos = 1.0
        self.player.set_position(pos)

    # Change posiiton relative from the current one, in seconds
    # Return the new position
    def seek(self, seconds):
        change_relative = seconds / self.get_duration()
        self.set_position_relative(self.get_position_relative() + change_relative)
        return self.get_position()

    # Go to the beginning of the previous file (if multiple loaded)
    # Return the number of the new file or -1 if there is no previous.
    def prev(self):
        if self.current <= 0:
            return -1

        was_playing = self.player.is_playing()
        self.stop()
        self.current -= 1
        self.init_media(self.current)
        if was_playing:
            self.player.play()
        return self.current

    # Go to the beginning of the next file (if multiple loaded)
    # Return the number of the new file or -1 if there is no next.
    def next(self):
        if (self.current + 1) >= self.num_files():
            return -1

        was_playing = self.player.is_playing()
        self.stop()
        self.current += 1
        self.init_media(self.current)
        if was_playing:
            self.player.play()
        return self.current

    # Start/Resume the playback from the current position
    def play(self):
        self.player.play()

    # Pause the playback and remember the current position
    def pause(self):
        self.player.pause()

    # Play or pause playback depening on current playback status
    def toggle_playback(self):
        if self.player.is_playing():
            self.pause()
        else:
            self.play()

    # Return `True` if currently playing, otherwise `False`
    def is_playing(self):
        return self.player.is_playing()

    # Halt playback and set position to 0
    def stop(self):
        self.player.stop()

    # Halt playback, free all resources, clean up after yourself
    def cleanup(self):
        self.stop()
        self.player.release()
        for m in self.media:
            m.release()
        self.media = []
        self.current = -1
