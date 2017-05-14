import vlc

class VLC():

    options = [
        "--aout=alsa",
        #"--novideo",
        #"--one-instance",
        #"--no-playlist-autostart",
        #"--playlist-enqueue"
    ]

    volume_def = 50
    volume_min = 0
    volume_max = 100

    def __init__(self):
        self.instance = vlc.Instance(" ".join(VLC.options))
        self.player = self.instance.media_list_player_new()
        self.media_list = self.instance.media_list_new()
        self.player.get_media_player().audio_set_volume(VLC.volume_def)
        self.current = 0

    # Load a given file. Frees all currently loaded files.
    # Return 1 on success, 0 on failure
    def load(self, file):        
        self.reset_player() # re-create the player
        self.reset_media()  # re-create the media_list

        self.add(file)    # Add the file to the media_list
        self.load_media() # Load the media_list into the player

    # Add a media file to the media list
    # Return 1 on success, 0 on failure
    def add(self, mrl):
        media = self.instance.media_new(mrl)
        if media.get_type() != vlc.MediaType.file:
            return 0
        if self.media_list.add_media(media) == 0:
            return 1
        else:
            return 0

    # Load a given list of files. Frees all currently loaded files.
    # Return the number of files loaded
    def load_all(self, files):
        # Empty list? Stop right there...        
        if len(files) == 0:
            return 0

        self.reset_player()
        self.reset_media()

        num_files_loaded = 0
        for file in files:
            num_files_loaded += self.add(file)
        self.load_media()
        return num_files_loaded

    # Return the number of loaded files
    def num_files(self):
        return self.media_list.count()
    
    # Return the file name of the current or specified file (by index)
    def get_filename(self, index=-1):
        if index == -1:
            index = self.current
        if index < 0 or index >= self.num_files():
            raise IndexError((self.__class__.__name__) + ".get_filename()")

        return self.media_list.item_at_index(index).get_mrl()

    # Return the name of the current or specified file's artist
    # This should be the author. If not set, return `None`
    def get_author(self, index=-1):
        if index == -1:
            index = self.current
        if index < 0 or index >= self.num_files():
            raise IndexError((self.__class__.__name__) + ".get_author()")

        artist = self.media_list.item_at_index(index).get_meta(vlc.Meta.Artist)
        
        if artist:
            return artist
        return None

    # Return the name of the current of specified file's title
    # This should be the title of the book. If not set, return `None`
    def get_title(self, index=-1):
        if index == -1:
            index = self.current
        if index < 0 or index >= self.num_files():
            raise IndexError((self.__class__.__name__) + ".get_title()")

        album = self.media_list.item_at_index(index).get_meta(vlc.Meta.Album)
        title = self.media_list.item_at_index(index).get_meta(vlc.Meta.Title)

        if album:
            return album
        if title:
            return title
        return None

    # Return the length (in seconds) of the current or specified file
    def get_duration(self, index=-1):
        if index == -1:
            index = self.current
        if index < 0 or index >= self.num_files():
            raise IndexError((self.__class__.__name__) + ".get_duration()")

        duration = self.media_list.item_at_index(index).get_duration() # ms, exact
        return duration // 1000 # s, rounded
    
    # Return the index of the current file
    def get_current(self):
        return self.current

    # Return the current volume [0..100]
    def get_volume(self):
        return self.player.get_media_player().audio_get_volume()

    # Set the volume to the specified value [0..100]
    # Return the new set volume
    def set_volume(self, volume):
        if volume < 0:
            volume = 0
        elif volume > 100:
            volume = 100
        self.player.get_media_player.audio_set_volume(volume)

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
        return self.player.get_media_player().get_position() # [0.0..1.0]

    # Set position with a relative value (range [0.0..0.1]
    def set_position_relative(self, pos):
        if pos < 0.0:
            pos = 0.0
        elif pos > 1.0:
            pos = 1.0
        self.player.get_media_player().set_position(pos)

    # Change posiiton relative from the current one, in seconds
    # Return the new position
    def seek(self, seconds):
        change_relative = seconds / self.get_duration()
        set_position_relative(get_position_relative() + change_relative)

    # Go to the beginning of the previous file (if multiple loaded)
    # Return the number of the new file or -1 if there is no previous.
    def prev():                
        if self.player.previous() == 0:
            self.current -= 1
            return self.current
        else:
            return -1

    # Go to the beginning of the next file (if multiple loaded)
    # Return the number of the new file or -1 if there is no next.
    def next():
        if self.player.next() == 0:
            self.current += 1
            return self.current
        else:
            return -1

    # Start/Resume the playback from the current position
    def play():
        self.player.play() # TODO does this play from the start or cur pos?

    # Pause the playback and remember the current position
    def pause():
        self.player.pause()

    # Play or pause playback depening on current playback status
    def toggle_playback():
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
            self.player = self.instance.media_list_player_new()

    # Halt playback, empty the playlist (free the files)
    def reset_media(self):
        if self.media_list:
            self.stop()
            self.media_list.release()
            self.media_list = self.instance.media_list_new()

    # Reload the media list into the player
    def load_media(self):
        self.player.set_media_list(self.media_list)
