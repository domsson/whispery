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

def btn_r_action(pin, event):
    global vlc
    if vlc.next() >= 0:
        print("next (" + str(vlc.get_current()) +  ")")
    else:
        print("n/a")

def btn_c_action(pin, event):
    global vlc
    if vlc.is_playing():
        vlc.pause()
        print("pausing")
    else:
        vlc.play()
        print("playing...")

def btn_l_action(pin, event):
    global vlc
    if vlc.prev() >= 0:
        print("prev (" + str(vlc.get_current()) + ")")
    else:
        print("n/a")

def btn_v_action(pin, event):
    global vlc
    print("pos: " + str(vlc.get_position()) + " s")

def btn_p_action(pin, event):
    global vlc
    vlc.stop()
    print("stopped.")

def rot_debug(event):
    print("rot event: " + str(event))

def rot_v_action(event):
    global vlc
    if event == RotaryEncoder.CW:
        print("vol = " + str(vlc.set_volume(vlc.get_volume() + 1)))
    elif event == RotaryEncoder.CCW:
        print("vol = " + str(vlc.set_volume(vlc.get_volume() - 1)))
    else:
        rot_debug(event)

def rot_p_action(event):
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

btn_l_pin = 24  # left button
btn_l_bnc = 300

btn_c_pin = 23  # center button
btn_c_bnc = 300

btn_r_pin = 17  # right button
btn_r_bnc = 300

btn_p_pin = 26  # pos rotary button
btn_p_bnc = 300

btn_v_pin = 16  # vol rotary button
btn_v_bnc = 300 

rot_p_pin1 = 11 # pos rotary encoder
rot_p_pin2 =  0

rot_v_pin1 =  7 # vol rotary encoder
rot_v_pin2 =  1

gpio.setmode(gpio.BCM)

btn_l = PushButton(gpio, btn_l_pin, btn_l_bnc, btn_l_action, name="btn_l")
btn_c = PushButton(gpio, btn_c_pin, btn_c_bnc, btn_c_action, name="btn_c")
btn_r = PushButton(gpio, btn_r_pin, btn_r_bnc, btn_r_action, name="btn_r")
btn_p = PushButton(gpio, btn_p_pin, btn_p_bnc, btn_p_action, name="btn_p")
btn_v = PushButton(gpio, btn_v_pin, btn_v_bnc, btn_v_action, name="btn_v")
rot_p = RotaryEncoder(gpio, rot_p_pin1, rot_p_pin2, rot_p_action, name="rot_p")
rot_v = RotaryEncoder(gpio, rot_v_pin1, rot_v_pin2, rot_v_action, name="rot_v")

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
