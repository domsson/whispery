#!/usr/bin/env python3

import os
import sys
import vlc
import time
import signal 
import RPi.GPIO as gpio 
from rotaryencoder import RotaryEncoder
from pushbutton import PushButton
from vlcplayer import VLCPlayer
from playerdisplay import PlayerDisplay

vlc = None
files = []
oled = None
debug = False
running = False
proceed = False
loading = False
last_input = 0 
exit_menu = False

AUDIO_AUTO = 0
AUDIO_JACK = 1
AUDIO_HDMI = 2

audio_device = AUDIO_AUTO

SHUTDOWN = -2
REBOOT = -1
EXIT = 0

on_exit = EXIT

#################
###   FUNCS   ###
#################

def log(text):
    if debug:
        print(text)

def abs_path(relative_path):
    return os.path.join(sys.path[0], relative_path)

def signal_handler(signal, frame):
    global running
    running = False

def get_media_path():
    #udisks_cfg = abs_path("udisks-glue.conf")
    #os.system("udisks-glue -c " + udisks_cfg)
    os.system("udisks-glue")
    time.sleep(3)
    mount_dir = "/media"
    for d in os.listdir(mount_dir):
        abs_dir = os.path.join(mount_dir, d)
        if os.path.isdir(abs_dir):
            if contains_audio_files(abs_dir):
                return abs_dir
    return abs_path("mp3")

def contains_audio_files(directory):
    for f in os.listdir(directory):
        if f.endswith(".mp3") or f.endswith(".ogg"):
            return True
    return False

def init_files(directory):
    global files
    for f in os.listdir(directory):
        if f.endswith(".mp3") or f.endswith(".ogg"):
            files.append(os.path.join(directory, f))
    files.sort()

def init_vlc():
    global vlc
    vlc = VLCPlayer(75)
    vlc.set_callback_track_end(on_track_end)

def init_inputs():
    global gpio
    gpio.setmode(gpio.BCM)

    btn_l_pin = 24  # left button
    btn_l_bnc = 300
    btn_c_pin = 23  # center button
    btn_c_bnc = 300
    btn_r_pin = 17  # right button
    btn_r_bnc = 300
    btn_p_pin = 16  # pos rotary button
    btn_p_bnc = 300
    btn_v_pin = 26  # vol rotary button
    btn_v_bnc = 300 
    rot_p_pin1 =  7 # pos rotary encoder
    rot_p_pin2 =  1
    rot_v_pin1 = 11 # vol rotary encoder
    rot_v_pin2 =  0

    btn_l = PushButton(gpio, btn_l_pin, btn_l_bnc, btn_l_action, name="btn_l")
    btn_c = PushButton(gpio, btn_c_pin, btn_c_bnc, btn_c_action, name="btn_c")
    btn_r = PushButton(gpio, btn_r_pin, btn_r_bnc, btn_r_action, name="btn_r")
    btn_p = PushButton(gpio, btn_p_pin, btn_p_bnc, btn_p_action, name="btn_p")
    btn_v = PushButton(gpio, btn_v_pin, btn_v_bnc, btn_v_action, name="btn_v")
    rot_p = RotaryEncoder(gpio, rot_p_pin1, rot_p_pin2, rot_p_action, name="rot_p")
    rot_v = RotaryEncoder(gpio, rot_v_pin1, rot_v_pin2, rot_v_action, name="rot_v")    

def init_oled():
    global oled
    oled = PlayerDisplay(abs_path("fonts"))

def display_loading_screen():
    global oled
    if not oled:
        return
    w = oled.get_num_chars_per_line()
    h = oled.get_num_lines()
                              #####################
    oled.draw_string(3, "       LOADING       ")
    oled.display()

def display_main_screen():
    global oled
    if not oled:
        return
    w = oled.get_num_chars_per_line()
    h = oled.get_num_lines()

    status = "stopped"
    if vlc.is_playing():
        status = "playing"

    oled.draw_string(0, vlc.get_author()[:w])
    oled.draw_string(1, vlc.get_title()[:w])
    oled.draw_string(2, "---------------------")
    oled.draw_string(3, "File: " + str(vlc.get_current() + 1) + " / " + str(vlc.num_files()))
    oled.draw_string(4, "Time: " + str(vlc.get_position()) + " / " + str(vlc.get_duration()))
    oled.draw_string(5, "Vol.: " + str(vlc.get_volume()) + " / 100")
    oled.draw_string(6, "---------------------")
    oled.draw_string(7, "     [ " + status + " ]     ")
    oled.display()

def display_exit_screen():
    global oled
    if not oled:
        return

    oled.draw_string(2, "---------------------")
    oled.draw_string(4, "      SHUTDOWN?      ")
    oled.draw_string(6, "---------------------")
    oled.draw_string(7, "[yes] [restart]  [no]")
    oled.display()

def on_track_end(event):
    # We can't call into libVLC from within the callback, so we'll take a detour
    log("Track ended, scheduling next track")
    global proceed
    proceed = True

def btn_r_action(pin, event):
    global running
    if not running:
        return

    global last_input
    global exit_menu
    global vlc

    last_input = time.time()
    if event != PushButton.PRESSED:
        return
    if exit_menu:
        exit_menu = False
        return
    if vlc.next() >= 0:
        log("next (" + str(vlc.get_current()) +  ")")
    else:
        log("n/a")

def btn_c_action(pin, event):
    global running
    if not running:
        return

    global last_input
    global vlc
    
    last_input = time.time()
    if event != PushButton.PRESSED:
        return
    if exit_menu:
        reboot()
        return
    if vlc.is_playing():
        vlc.pause()
        log("pausing")
    else:
        vlc.play()
        log("playing...")

def btn_l_action(pin, event):
    global running
    if not running:
        return

    global last_input
    global exit_menu
    global vlc

    last_input = time.time()
    if event != PushButton.PRESSED:
        return
    if exit_menu:
        shutdown()
        return
    if vlc.prev() >= 0:
        log("prev (" + str(vlc.get_current()) + ")")
    else:
        log("n/a")

def btn_v_action(pin, event):
    global running
    if not running:
        return

    global last_input
    global exit_menu
    global vlc

    last_input = time.time()
    if event != PushButton.PRESSED:
        return

    exit_menu = True
    log("pos: " + str(vlc.get_position()) + " s")

def btn_p_action(pin, event):
    global running
    if not running:
        return

    global last_input
    last_input = time.time()
    if event != PushButton.PRESSED:
        return
    if exit_menu:
        reload()
        return
    else:
        log("Toggling audio output device")
        toggle_audio_jack()

def rot_v_action(event):
    global running
    if not running:
        return
    
    global last_input
    global vlc
    
    last_input = time.time()
    if event == RotaryEncoder.CW:
        log("vol = " + str(vlc.set_volume(vlc.get_volume() + 1)))
    elif event == RotaryEncoder.CCW:
        log("vol = " + str(vlc.set_volume(vlc.get_volume() - 1)))

def rot_p_action(event):
    global running
    if not running:
        reutnr
    
    global last_input
    last_input = time.time()
    global vlc
    if event == RotaryEncoder.CW:
        log("pos: " + str(vlc.seek( 30)) + " / " + str(vlc.get_duration()))
    elif event == RotaryEncoder.CCW:
        log("pos: " + str(vlc.seek(-30)) + " / " + str(vlc.get_duration()))

def toggle_audio_jack():
    global audio_device
    if audio_device == AUDIO_AUTO:
        set_audio_out(AUDIO_JACK)
    else:
        set_audio_out(AUDIO_AUTO)

def set_audio_out(audio):
    global audio_device
    selection = None
    
    if audio == AUDIO_AUTO:
        selection = "auto select"
    elif audio == AUDIO_JACK:
        selection = "headphone jack"
    elif audio == AUDIO_HDMI:
        selection = "HDMI"
    
    if selection:
        log("Setting audio output to " + selection)
        os.system("amixer cset -q numid=3 " + str(audio))
        audio_device = audio
    else:
        log("Tried to set audio output to invalid value, did nothing")

def reload():
    global vlc
    global files
    global loading
    global exit_menu

    loading = True
    exit_menu = False
    vlc.stop()
    vlc.cleanup()
    vlc = None

    init_files(abs_path(get_media_path()))
    init_vlc()
    vlc.load_all(files)
    loading = False

def cleanup():
    global vlc
    global gpio
    global oled
    oled.cleanup()
    gpio.cleanup()
    vlc.cleanup()

def reboot():
    global running
    global on_exit
    global REBOOT
    on_exit = REBOOT
    running = False

def shutdown():
    global running
    global on_exit
    global SHUTDOWN
    on_exit = SHUTDOWN
    running = False

################
###   MAIN   ###
################

# Make sure CTRL+C will lead to a cleanup
signal.signal(signal.SIGINT, signal_handler)

if "-d" in sys.argv:
    debug = True

loading = True

log("Setting audio output to 'auto'...")
set_audio_out(AUDIO_AUTO)
log("Initializing GPIO...")
init_inputs()
log("Initializing OLED display...")
init_oled()
log("Displaying loading screen...")
display_loading_screen()
log("Scanning for mounted media...")
media_path = get_media_path()
log("Scanning for audio files...")
init_files(abs_path(media_path))

if len(files) > 0:
    log("Found " + str(len(files)) + " files.")
    log("Initializing VLC...")
    init_vlc()
    log("Loading audio files...")
    vlc.load_all(files)
    running = True

log("Ready!")
last_input = time.time()
loading = False

while running:
    oled.clear()
    now = time.time()
    if (now - last_input) < 10:
        if exit_menu:
            display_exit_screen()
        elif loading:
            display_loading_screen()
        else:
            display_main_screen()
    else:
        oled.display()
    if proceed:
        log("Track ended, scheduling next track")
        proceed = False
        vlc.next()
        vlc.play()
    time.sleep(0.1)

cleanup()
time.sleep(1)

if on_exit == REBOOT:
    #log("Rebooting device, bye!")
    #os.system("sudo shutdown -r now")
    os.system("/home/pi/workspace/whispery/whispery.py &")
    sys.exit(0)
elif on_exit == SHUTDOWN:
    log("Shutting down device, bye!")
    os.system("sudo shutdown -h now")
    sys.exit(0)
else:
    log("Exiting ABP, bye!")
    sys.exit(0)
