#!/usr/bin/env python3

import sys
import vlc
import time
import signal 
import RPi.GPIO as gpio 
from rotary_class import RotaryEncoder
from pbutton_class import PushButton
from vlc_class import VLC

vlc = None
running = False

def init_vlc():
    global vlc
    vlc = VLC()
    files = [
            "mp3/whisperingeye_01_fleming-roberts_64kb.mp3",
            "mp3/whisperingeye_02_fleming-roberts_64kb.mp3",
            "mp3/whisperingeye_03_fleming-roberts_64kb.mp3",
            "mp3/whisperingeye_04_fleming-roberts_64kb.mp3",
            "mp3/whisperingeye_05_fleming-roberts_64kb.mp3",
            "mp3/whisperingeye_06_fleming-roberts_64kb.mp3",
            "mp3/whisperingeye_07_fleming-roberts_64kb.mp3",
            "mp3/whisperingeye_08_fleming-roberts_64kb.mp3",
            "mp3/whisperingeye_09_fleming-roberts_64kb.mp3",
            "mp3/whisperingeye_10_fleming-roberts_64kb.mp3"
    ]
    num_files = vlc.load_all(files)

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

def rot1_action(event):
    global vlc
    if event == RotaryEncoder.CW:
        print("vol = " + str(vlc.set_volume(vlc.get_volume() + 1)))
    elif event == RotaryEncoder.CCW:
        print("vol = " + str(vlc.set_volume(vlc.get_volume() - 1)))
    else:
        print("rot1 x")

def rot2_action(event):
    if event == RotaryEncoder.CW:
        print("pos: " + str(vlc.seek( 30)) + " / " + str(vlc.get_duration()))
    elif event == RotaryEncoder.CCW:
        print("pos: " + str(vlc.seek(-30)) + " / " + str(vlc.get_duration()))
    else:
        print("rot2 x")

signal.signal(signal.SIGINT, signal_handler)

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

pin_btn5 = 21
bnc_btn5 = 300 

rot1_pin1 = 11
rot1_pin2 = 0

rot2_pin1 = 20
rot2_pin2 = 16

gpio.setmode(gpio.BCM)

btn1 = PushButton(gpio, pin_btn1, bnc_btn1, btn1_action)
btn2 = PushButton(gpio, pin_btn2, bnc_btn2, btn2_action)
btn3 = PushButton(gpio, pin_btn3, bnc_btn3, btn3_action)
btn4 = PushButton(gpio, pin_btn4, bnc_btn4, btn4_action)
btn5 = PushButton(gpio, pin_btn5, bnc_btn5, btn5_action)
rot1 = RotaryEncoder(gpio, rot1_pin1, rot1_pin2, rot1_action)
rot2 = RotaryEncoder(gpio, rot2_pin1, rot2_pin2, rot2_action)

sys.stdout.write("done\n")
sys.stdout.flush()

print_vlc_info()

while running:
    time.sleep(1)

sys.stdout.write("Shutdown initialized... ")
cleanup()
sys.stdout.write("done. Bye!\n")
sys.stdout.flush()
sys.exit(0)
