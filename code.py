import time
import board
import touchio
import neopixel
import adafruit_fancyled.adafruit_fancyled as fancy

num_pixels = 30

# pin usage: TRINKET: board.D4, GEMMA: board.D1
strip = neopixel.NeoPixel( board.D1, num_pixels, brightness = 0.25, auto_write = False )

print( "FancyPole Gemma M0" )

# refer to
# https://learn.adafruit.com/fancyled-library-for-circuitpython/led-colors
# across the rainbow
grad = [ (0.0,0xFF0000), (0.33,0x00FF00), (0.67,0x0000FF), (1.0,0xFF0000)]
palette = fancy.expand_gradient( grad, 20 )

onoff = True
offset = 0.001

def color_selected() :
    # pick the center color and fill the strip with that color statically displayed
    colorindex = offset + 0.5
    return fancy.palette_lookup( palette, colorindex )

def show_static() :
    color = color_selected()
    strip.fill( color.pack() )
    strip.show()

def palette_cycle() :
    for i in range( num_pixels ) :
        colorindex = offset + ( i / num_pixels )
        color = fancy.palette_lookup( palette, colorindex )
        strip[i] = color.pack()
    strip.show()


class TouchMode :
    def __init__( self, pin, lastmode = 1, name = None ) :
        self.mode = 0
        self.lastmode = lastmode
        self.touch = touchio.TouchIn( pin )
        self.name = name or "mode"

    def exec( self ) :
        wasoff = not self.touch.value
        time.sleep(0.005)  # 5ms delay for debounce
        if not wasoff and self.touch.value :
            # just touched button
            time.sleep(0.005)  # 5ms delay for debounce
            if self.mode >= self.lastmode :
                self.mode = 0
            else :
                self.mode = self.mode + 1
            # debounce
            time.sleep( 0.5 )
            print( self.name + " {}".format( self.mode ) )
        return self.mode

# OnOff pin usage: TRINKET: board.A0, GEMMA: board.A1
# Mode pin usage: TRINKET: board. TBD ??, GEMMA: board.A2

onoffMachine = TouchMode( board.A1, 1, "onoff" )
modeMachine = TouchMode( board.A2, 2 )

# Loop Forever
while True :
    if onoffMachine.exec() == 0 :
        palette_cycle()
        offset += 0.035 # this sets how quickly the rainbow changes (bigger is faster)
    else :
        mode = modeMachine.exec()
        if mode == 0 :
            # and if just off just off paint/fill w/ the center color
            show_static()
        else :
            show_static()