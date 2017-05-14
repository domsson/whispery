import vlc

class VLC():

    options = [
        "--aout=alsa",
        "--novideo",
        #"--one-instance",
        #"--no-playlist-autostart",
        #"--playlist-enqueue"
    ]

    volume_def = 50
    volume_min = 0
    volume_max = 100

    def __init__(self):
        self.instance = vlc.Instance(" ".join(VLC.options))
        self.player = self.instance.media_player_new()
        self.player.audio_set_volume(VLC.volume_def)
        self.media = None
        self.files = []
        self.current = -1

    # Turn the selected file into media to make it the current file
    # This is required in order to play the selected file
    def init_media(self, index):
        if index < 0 or index >= len(self.files):
            raise IndexError((self.__class__.__name__) + ".get_filename()")
        self.media = self.instance.media_new(self.files[index])

    # Load a given file. Frees all currently loaded files.
    # Return 1 on success, 0 on failure
    def load(self, file):
        self.files = []
        self.reset_player() # re-create the player
        self.reset_media()  # release the media
        self.current = -1

        self.add(file)      # Add the file to the media_list
        self.init_media(0)  # Turn the file into media
        self.load_media()   # Load the media into the player

    # Add a media file to the media list
    # Returns the number of files in the file list
    def add(self, mrl):
        self.files.append(mrl)
        if self.current == -1:
            self.current = 0
        return len(self.files)

    # Add all given media files to the media list
    # Returns the number of files in the file list
    def add_all(self, mrls):
        for mrl in mrls:
            self.files.append(mrl)
        if self.current == -1:
            self.current = 0
        return len(self.files)

    # Load a given list of files. Frees all currently loaded files.
    # After this operation, the first of the given files will be ready to play.
    # Return the number of files loaded
    def load_all(self, files):        
        if len(files) == 0:
            return 0

        self.files = []
        self.reset_player()
        self.reset_media()
        self.current = -1

        num_files = self.add_all(files)
        self.init_media(0)
        self.load_media()
        return num_files

    # Return the number of loaded files
    def num_files(self):
        return len(self.files)
    
    # Return the file name of the current or specified file (by index)
    def get_filename(self, index=-1):
        if not media:
            # TODO
            print("warning: no media initialized yet!")
        if index == -1:
            index = self.current
        if index < 0 or index >= self.num_files():
            raise IndexError((self.__class__.__name__) + ".get_filename()")

        return self.files[index]

    # Return the name of the current or specified file's artist
    # This should be the author. If not set, return `None`
    def get_author(self, index=-1):
        if not media:
            # TODO
            print("warning: no media initialized yet!")
        if index == -1:
            index = self.current
        if index < 0 or index >= self.num_files():
            raise IndexError((self.__class__.__name__) + ".get_author()")

        artist = ""
        if index == current:
            artist = self.media.get_meta(vlc.Meta.Artist)
        else:
            temp_media = self.instance.media_new(self.files[index])
            artist = media.get_meta(vlc.Meta.Artist)

        if artist:
            return artist
        return None

    # Return the name of the current of specified file's title
    # This should be the title of the book. If not set, return `None`
    def get_title(self, index=-1):
        if not media:
            # TODO
            print("warning: no media initialized yet!")
        if index == -1:
            index = self.current
        if index >= self.num_files():
            raise IndexError((self.__class__.__name__) + ".get_title()")

        album = ""
        title = ""

        if index == current:
            album = self.media.get_meta(vlc.Meta.Album)
            title = self.media.get_meta(vlc.Meta.Title)
        else:
            temp_media = self.instance.media_new(self.files[index])
            album = temp_media.get_meta(vlc.Meta.Album)
            title = temp_media.get_meta(vlc.Meta.Title)

        if album:
            return album
        if title:
            return title
        return None

    # Return the length (in seconds) of the current or specified file
    def get_duration(self, index=-1):
        if not media:
            # TODO
            print("warning: no media initialized yet!")
        if index == -1:
            index = self.current
        if index < 0 or index >= self.num_files():
            raise IndexError((self.__class__.__name__) + ".get_duration()")

        duration = self.media.get_duration() # ms, exact
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
        set_position_relative(get_position_relative() + change_relative)

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
        if self.current > self.num_files():
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
        self.player.play() # TODO does this play from the start or cur pos?

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
        self.player.stop() # TODO does this reset the pos to start?

    # Halt playback, free all resources, clean up after yourself
    def cleanup(self):
        self.stop()
        self.reset_player()
        self.reset_media()
        self.current = 0

    # Halt playback, release the player
    def reset_player(self):
        if self.player:
            self.stop()
            self.player.release()
            self.player = self.instance.media_player_new()

    # Halt playback, empty the playlist (free the files)
    def reset_media(self):
        if self.media:
            self.stop()
            self.media.release()
            self.media = None

    # Reload the media list into the player
    def load_media(self):
        if self.media:
            self.player.set_media(self.media)
