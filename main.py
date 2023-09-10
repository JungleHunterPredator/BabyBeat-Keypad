# CTRL + D = reload
# CTRL + C = enter REPL

from pmk import PMK
from pmk.platform.rgbkeypadbase import RGBKeypadBase as Hardware
import usb_midi
import adafruit_midi
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on import NoteOn
import time
import random

keypico = PMK(Hardware())
keys = keypico.keys

midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], 
                          out_channel=0)

# Colour selection
snow = (0, 0, 0)
blue = (0, 0, 255)
cyan = (0, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
purple = (255, 0, 255)

def randomRGB():
    r = random.choice([0, 128, 255])
    g = random.choice([0, 128, 255])
    b = random.choice([0, 128, 255])
    return (r, g, b)

# Set key colours for all keys
keypico.set_all(*snow)

# Orientation
# keypico.set_led(0, *red)
# keypico.set_led(3, *green)
# keypico.set_led(12, *blue)
# keypico.set_led(15, *purple)

# Set sleep time
keypico.led_sleep_enabled = True
keypico.led_sleep_time = 10

# Midi

start_note = 68
velocity = 127

dangerKey = [3, 2, 1, 0]
pressedKey = []

def danger():
    if len(pressedKey) == 4:
        if pressedKey == dangerKey:
            for i in range (3):
                red = (255, 0, 0)
                time.sleep(1)
                for key in keys:
                    key.set_led(*red)
                time.sleep(1)
                for key in keys:
                    key.set_led(*snow)
        else:
            pressedKey = []
    else:
        pressedKey = []

# Loop

for key in keys:
    held = False

    @keypico.on_press(key)
    def press_handler(key):
        RGBp = randomRGB()
        
        print("Key {} pressed".format(key.number))
        key.set_led(*RGBp)
        note = start_note + key.number
        pressedKey.append(key.number)
        print(pressedKey)
        print(len(pressedKey))
        print(type(len(pressedKey)))

        midi.send(NoteOn(note, velocity))

    @keypico.on_release(key)
    def release_handler(key):
        RGBh = randomRGB()
        print("Key {} released".format(key.number))
        key.set_led(*RGBh)
        note = start_note + key.number
        midi.send(NoteOff(note, 0))

    @keypico.on_hold(key)
    def hold_handler(key):
        RGBr = randomRGB()
        print("Key {} held".format(key.number))
        key.set_led(*RGBr)

while True:
    keypico.update()

