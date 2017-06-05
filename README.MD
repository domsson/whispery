Raspberry Pi Audio Book Player
==============================

This is supposed to be a python script powering an audio book player using the Rasperry Pi, three push buttons, two rotary encoders (with push buttons) and a 128x64 pixel OLED display.

Dependencies / Software setup
-----------------------------

Requires `python3` and the `libvlc` bindings for it, namely `python-vlc`.
Also requires the `Adafruit_SSD1306` python library.
And some other stuff I forgot about.

Notes
-----

Using the audio jack with some speakers or headphones might yield a very low volume by default. Setting ALSA's volume to 100% helps:

    amixer set PCM -- 100%

Also, the Rasperry will, by default, send audio through HDMI if there is a device connected there. However, during development, it can be helpful to force the audio through the audio jack, for example when the Pi is hooked up to a TV for coding purposes, but sound is supposed to come out of speakers connected to the audio jack. For that, these `amixer` commands can be used:

    amixer cset numid=3 0
    amixer cset numid=3 1
    amixer cset numid=3 2

Where `0` is `auto`, `1` is `jack` and `2` is `hdmi`.

To start _whispery_ on boot, it is recommended to use `crontab` with the regular user (`pi`), as using `rc.local` can lead to permission issues in combination with `udisks-glue`.

    contab -e
    @reboot /home/pi/workspace/whispery/whispery.py &
