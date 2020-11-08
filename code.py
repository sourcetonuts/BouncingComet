import time
import board
import adafruit_dotstar as dotstar
import adafruit_fancyled.adafruit_fancyled as fancy

num_pixels = 54
strip = dotstar.DotStar( board.SCK, board.MOSI, num_pixels, brightness=1.0, auto_write=False )
print( "BouncingComet" )

# refer to for gradiant / color info
# https://learn.adafruit.com/fancyled-library-for-circuitpython/led-colors

class Comet( object ) :
    def __init__( self, strip ) :
        self.strip = strip
        self.reset()

    def reset( self ) :
        self.BLACK = (0,0,0)
        self.hue = 5
        self.sat = 1.0
        self.bri = 1.0
        self.satdelta = 0.05
        self.up = True
        self.indexLast = strip.n - 1
        self.length = 5
        self.current = 0
        self.delay = 0.0
        strip.fill( self.BLACK )
        strip.show()

    def animate( self ) :
        if self.up :
            self.draw_up()
        else :
            self.draw_down()
        time.sleep( self.delay )
        self.next()

    def draw_up( self ) :
        next = self.current
        end = next + self.length
        nextsat = self.sat - ( ( self.length - 1 ) * self.satdelta )

        if ( next >= 0 ) :
            strip[next] = self.BLACK

        while ( next < end ) :
            nextsat = nextsat + self.satdelta
            color = fancy.CHSV(self.hue,nextsat,self.bri)
            next = next + 1
            self.strip[next] = color.pack()

        self.strip.show()

    def draw_down( self ) :
        next = self.current
        end = next + self.length
        nextsat = self.sat

        while ( next < end ) :
            color = fancy.CHSV(self.hue,nextsat,self.bri)
            next = next + 1
            self.strip[next] = color.pack()
            nextsat = nextsat - self.satdelta

        next = next + 1
        if next <= self.indexLast :
            self.strip[next] = self.BLACK
        self.strip.show()

    def next( self ) :
        if self.up :
            self.delay = self.delay + ( self.current * 0.0001 ) # 0.002
            self.current = self.current + 1
        else :
            self.delay = self.delay - ( self.current * 0.0001 ) # 0.002
            self.current = self.current - 1

        if ( self.delay < 0 ) :
            self.delay = 0

        if ( self.up and ( self.current + self.length ) > self.indexLast ) :
            self.up = False
            self.current = self.indexLast - self.length
        elif ( not self.up and self.current == 0 ) :
            self.up = True

print( "strip {} pixels".format( strip.n ) )
comet = Comet( strip )

# Loop Forever
while True :
    comet.animate()