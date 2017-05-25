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
running = False
proceed = False
last_input = 0 

#################
###   FUNCS   ###
#################

def abs_path(relative_path):
    return os.path.join(sys.path[0], relative_path)

def signal_handler(signal, frame):
    global running
    running = False

def init_files(directory):
    global files
    for f in os.listdir(directory):
        if f.endswith(".mp3") or f.endswith(".ogg"):
            files.append(os.path.join(directory, f))
    files.sort()

def init_vlc():
    global vlc
    #global files
    vlc = VLCPlayer(100)
    #vlc.load_all(files)
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

def on_track_end(event):
    # We can't call into libVLC from within the callback, so we'll take a detour
    global proceed
    proceed = True

def btn_r_action(pin, event):
    global last_input
    last_input = time.time()
    global vlc
    if event != PushButton.PRESSED:
        return
    if vlc.next() >= 0:
        print("next (" + str(vlc.get_current()) +  ")")
    else:
        print("n/a")

def btn_c_action(pin, event):
    global last_input
    last_input = time.time()
    global vlc
    if event != PushButton.PRESSED:
        return
    if vlc.is_playing():
        vlc.pause()
        print("pausing")
    else:
        vlc.play()
        print("playing...")

def btn_l_action(pin, event):
    global last_input
    last_input = time.time()
    global vlc
    if event != PushButton.PRESSED:
        return
    if vlc.prev() >= 0:
        print("prev (" + str(vlc.get_current()) + ")")
    else:
        print("n/a")

def btn_v_action(pin, event):
    global last_input
    last_input = time.time()
    global vlc
    print("pos: " + str(vlc.get_position()) + " s")

def btn_p_action(pin, event):
    global last_input
    last_input = time.time()
    global vlc
    vlc.stop()
    print("stopped.")

def rot_v_action(event):
    global last_input
    last_input = time.time()
    global vlc
    if event == RotaryEncoder.CW:
        print("vol = " + str(vlc.set_volume(vlc.get_volume() + 1)))
    elif event == RotaryEncoder.CCW:
        print("vol = " + str(vlc.set_volume(vlc.get_volume() - 1)))

def rot_p_action(event):
    global last_input
    last_input = time.time()
    global vlc
    if event == RotaryEncoder.CW:
        print("pos: " + str(vlc.seek( 30)) + " / " + str(vlc.get_duration()))
    elif event == RotaryEncoder.CCW:
        print("pos: " + str(vlc.seek(-30)) + " / " + str(vlc.get_duration()))

def cleanup():
    global vlc
    global gpio
    global oled
    gpio.cleanup()
    oled.cleanup()
    vlc.cleanup()


################
###   MAIN   ###
################

# Make sure CTRL+C will lead to a cleanup
signal.signal(signal.SIGINT, signal_handler)

print("Running from " + sys.path[0])
print("Font path: " + abs_path("fonts"))

print("Initializing GPIO...")
init_inputs()
print("Initializing OLED display...")
init_oled()
print("Displaying loading screen...")
display_loading_screen()
print("Scanning for audio files...")
init_files(abs_path("mp3"))

if len(files) > 0:
    print("Found " + str(len(files)) + " files.")
    print("Initializing VLC...")
    init_vlc()
    print("Loading audio files...")
    vlc.load_all(files)
    running = True

last_input = time.time()

while running:
    oled.clear()
    now = time.time()
    if (now - last_input) < 10:
        display_main_screen()
    else:
        oled.display()
    if proceed:
        print("Track ended, scheduling next track")
        proceed = False
        vlc.next()
        vlc.play()
    time.sleep(0.2)

print("Shutting down, bye bye!")
cleanup()
sys.exit(0)
