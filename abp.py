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

vlc = None
files = []
running = False
proceed = False

def read_mp3s():
    global files
    for file in os.listdir("mp3"):
        if file.endswith(".mp3") or file.endswith(".ogg"):
            files.append(os.path.join("mp3", file))
    files.sort()

def init_vlc():
    global vlc
    global files
    vlc = VLCPlayer(100)
    vlc.load_all(files)
    vlc.set_callback_track_end(on_track_end)

def print_vlc_info():
    global vlc
    print("Number of files in playlist: " + str(vlc.num_files()))
    print("Volume: " + str(vlc.get_volume()))
    print("Track: " + str(vlc.get_current()) + "(" + str(vlc.get_duration()) + " s)")
    print("File: " + vlc.get_filename())
    print("Author: " + vlc.get_author())
    print("Title: " + vlc.get_title())
    if vlc.is_playing():
        print("Status: playing")
    else:
        print("Status: stopped/paused")

def on_track_end(event):
    global proceed
    print("Track ended, scheduling next track")
    proceed = True

def signal_handler(signal, frame):
    global running
    running = False

def cleanup():
    global vlc
    gpio.cleanup()
    vlc.cleanup()

def btn1_action(pin, event):
    global vlc
    if vlc.next() >= 0:
        print("next (" + str(vlc.get_current()) +  ")")
    else:
        print("n/a")

def btn2_action(pin, event):
    global vlc
    if vlc.is_playing():
        vlc.pause()
        print("pausing")
    else:
        vlc.play()
        print("playing...")

def btn3_action(pin, event):
    global vlc
    if vlc.prev() >= 0:
        print("prev (" + str(vlc.get_current()) + ")")
    else:
        print("n/a")

def btn4_action(pin, event):
    global vlc
    print("pos: " + str(vlc.get_position()) + " s")

def btn5_action(pin, event):
    global vlc
    vlc.stop()
    print("stopped.")

def rot_debug(event):
    print("rot event: " + str(event))

def rot1_action(event):
    global vlc
    if event == RotaryEncoder.CW:
        print("vol = " + str(vlc.set_volume(vlc.get_volume() + 1)))
    elif event == RotaryEncoder.CCW:
        print("vol = " + str(vlc.set_volume(vlc.get_volume() - 1)))
    else:
        rot_debug(event)

def rot2_action(event):
    global vlc
    if event == RotaryEncoder.CW:
        print("pos: " + str(vlc.seek( 30)) + " / " + str(vlc.get_duration()))
    elif event == RotaryEncoder.CCW:
        print("pos: " + str(vlc.seek(-30)) + " / " + str(vlc.get_duration()))
    else:
        rot_debug(event)

signal.signal(signal.SIGINT, signal_handler)

read_mp3s()

sys.stdout.write("Initializing audio player... ")
init_vlc()
sys.stdout.write("done\n")
sys.stdout.flush()

running = True

sys.stdout.write("Initializing GPIO... ")

pin_btn1 = 15
bnc_btn1 = 300

pin_btn2 = 27
bnc_btn2 = 300

pin_btn3 = 10
bnc_btn3 = 300

pin_btn4 = 5
bnc_btn4 = 300 

pin_btn5 = 26
bnc_btn5 = 300 

rot1_pin1 = 11
rot1_pin2 =  0

rot2_pin1 =  7 
rot2_pin2 =  1

gpio.setmode(gpio.BCM)

btn1 = PushButton(gpio, pin_btn1, bnc_btn1, btn1_action, name="btn1")
btn2 = PushButton(gpio, pin_btn2, bnc_btn2, btn2_action, name="btn2")
btn3 = PushButton(gpio, pin_btn3, bnc_btn3, btn3_action, name="btn3")
#btn4 = PushButton(gpio, pin_btn4, bnc_btn4, btn4_action, name="btn4")
#btn5 = PushButton(gpio, pin_btn5, bnc_btn5, btn5_action, name="btn5")
rot1 = RotaryEncoder(gpio, rot1_pin1, rot1_pin2, rot1_action, name="rot1")
rot2 = RotaryEncoder(gpio, rot2_pin1, rot2_pin2, rot2_action, name="rot2")

sys.stdout.write("done\n")
sys.stdout.flush()

print_vlc_info()

while running:
    if proceed:
        proceed = False
        vlc.next()
        vlc.play()
    time.sleep(1)

sys.stdout.write("Shutdown initialized... ")
cleanup()
sys.stdout.write("done. Bye!\n")
sys.stdout.flush()
sys.exit(0)
