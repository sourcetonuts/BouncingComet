import time
import board
import touchio
from digitalio import DigitalInOut, Direction, Pull
import neopixel
import adafruit_fancyled.adafruit_fancyled as fancy

# GEMMA M0 wiring
#   USB micro for power
#   pin 6 aka A2 to touch button/copper pad
#   pin 2 aka D1 to NeoPixel data input pin
#   along with USB and GND from the Trinket for NeoPixel power/ground/data-in 3 conductor cable

# Gemma M0 pins
pin_leddata = board.D1
pin_touch = board.A1

# TRINKET M0
# with the following 96 LED setup on an Adafruit Trinket M0
# it could be wired up to run off of a basic/standard USB charger or laptop
# cabling required for Trinket
#   USB micro for power
#   pin 1 to touch button/copper pad
#   pin 4 to NeoPixel data input pin
#   along with USB and GND from the Trinket for NeoPixel power/ground/data-in 3 conductor cable

# Trinket M0 pins
# pin_leddata = board.D4
# pin_touch = board.A0

print( "FancyPole Gemma M0" )
num_pixels = 30
strip = neopixel.NeoPixel( pin_leddata, num_pixels, brightness = 0.25, auto_write = False )
touch = touchio.TouchIn( pin_touch )

# refer to
# https://learn.adafruit.com/fancyled-library-for-circuitpython/led-colors
# across the rainbow
grad = [ (0.0,0xFF0000), (0.33,0x00FF00), (0.67,0x0000FF), (1.0,0xFF0000)]
palette = fancy.expand_gradient( grad, 20 )

# todo read in these as stored from NVM or Drive or ?
onoff = True
offset = 0.001

def show_static() :
    print("show_static()")
    # pick the center color and fill the strip with that color statically displayed
    colorindex = offset + 0.5
    color = fancy.palette_lookup( palette, colorindex )
    strip.fill( color.pack() )
    strip.show()
    print( "offset: {}".format(offset) )

def palette_cycle() :
    for i in range( num_pixels ) :
        colorindex = offset + ( i / num_pixels )
        color = fancy.palette_lookup( palette, colorindex )
        strip[i] = color.pack()
        if touch.value :
            return
    strip.show()

# Loop Forever
while True :
    if onoff :
        # cycle the rainbow when on
        palette_cycle()
        offset += 0.035 # this sets how quickly the rainbow changes (bigger is faster)

    # deal onoff w/ button presses...
    wason = not touch.value
    time.sleep(0.005)  # 5ms delay for debounce
    if not wason and touch.value :
        # just touched mode button
        time.sleep(0.005)  # 5ms delay for debounce
        onoff = not onoff # toggle onoff state

        if onoff :
            print("rainbow")
        else :
            # and if just off just off paint/fill w/ the center color
            show_static()

        time.sleep( 0.5 )  # big delay so we dont 2x trigger button presses