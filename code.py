import time
import board
import microcontroller
from digitalio import DigitalInOut, Direction, Pull
import adafruit_dotstar as dotstar
import adafruit_fancyled.adafruit_fancyled as fancy

# with the following 96 LED setup on an Adafruit Trinket M0
# it could be wired up to run off of a basic/standard USB charger or laptop
# cabling required for Trinket
#   USB micro for power
#   pin 1 to touch button/copper pad
#   pin 3 to Dotstar clock input pin
#   pin 4 to Dotstar data input pin
#   along with USB and GND from the Trinket for NeoPixel power/ground/data-in 3 conductor cable

pin_touch = board.A0
pin_status = board.D13

num_pixels = 54
strip = dotstar.DotStar( board.SCK, board.MOSI, num_pixels, brightness=1.0, auto_write=False )
print( "BouncingComet" )

# refer to for gradiant / color info
# https://learn.adafruit.com/fancyled-library-for-circuitpython/led-colors


start = 0
length = 5
BLACK = (0,0,0)

hue = 0.0
sat = 1.0
bri = 0.4

delay = 0.002
satdelta = 0.08

strip.fill(BLACK);
strip.show();

def draw_comet_up() :
    next = start
    end = start + length
    nextsat = sat - ( ( length - 1 ) * satdelta )

    if ( next >= 0 ) :
        strip[next] = BLACK

    while ( next < end ) :
        nextsat = nextsat + satdelta
        color = fancy.CHSV(hue,nextsat,bri)
        next = next + 1
        strip[next] = color.pack()

    strip.show()


def draw_comet_down() :
    next = start
    end = start + length
    nextsat = sat

    while ( next < end ) :
        color = fancy.CHSV(hue,nextsat,bri)
        next = next + 1
        strip[next] = color.pack()
        nextsat = nextsat - satdelta

    next = next + 1
    if ( next <= last_index ) :
        strip[next] = BLACK
    strip.show()


up = True
last_index = num_pixels - 1

# Loop Forever
while True :
    time.sleep( delay )

    if up :
        draw_comet_up()
        start = start + 1
        delay = delay + 0.004
    else :
        draw_comet_down()
        start = start - 1
        delay = delay - 0.004

    if ( ( start + length ) >= last_index ) :
        up = False
    elif ( start == 0 ) :
        up = True