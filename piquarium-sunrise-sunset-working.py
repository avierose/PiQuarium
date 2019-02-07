import time
import datetime
import board
import neopixel


'''Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
NeoPixels must be connected to D10, D12, D18 or D21 to work.
'''
pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 30
max_bright = 5
min_bright = 0
step = 1
delay = 1

#Colour Values
global WR
global WG
global WB

'''The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
'''
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(pixel_pin, num_pixels,
                           brightness=1,
                           auto_write=False,
                           pixel_order=ORDER)

redpix = []
bluepix = []
whitepix = []

for pix in range(num_pixels):
    if pix % 4 == 0:                     ## every 4th number from 0
        redpix.append(pix)
    elif pix % 4 == 1:                   ## every 4th number from 1
        bluepix.append(pix)
    else:                              ## all other positions in the range
        whitepix.append(pix)
    
        
def red_pixels(r=0, g=0, b=0):
    print("Begin - Red RGB values are {}/{}/{}".format(r,g,b))
    while r < max_bright:
        if r < max_bright: r += step
        
        for pos in redpix:
            pixels[pos] = (r, g, b)
            pixels.show()
            print('(Pixel {}) = (R:{}, G:{}, B:{})'.format(pos, r, g, b))
        time.sleep(delay)
        
def red_pixels_down(r=max_bright, g=0, b=0):
    print("Begin - Red RGB values are {}/{}/{}".format(r, g, b))
    while r > min_bright:
        if r > min_bright: r -= step
        
        for pos in redpix:
            pixels[pos] = (r, g, b)
            pixels.show()
            print('(Pixel {}) = (R:{}, G:{}, B:{})'.format(pos, r, g, b))
        time.sleep(delay)

def blue_pixels(r=0, g=0, b=0):
    print("Begin - blue RGB values are {}/{}/{}".format(r,g,b))
    while b < max_bright:
        if b < max_bright: b += step
        
        for pos in bluepix:
            pixels[pos] = (r, g, b)
            pixels.show()
            print('(Pixel {}) = (R:{}, G:{}, B:{})'.format(pos, r, g, b))
        time.sleep(delay)

def blue_pixels_down(r=0, g=0, b=max_bright):
    print("Begin - Blue RGB values are {}/{}/{}".format(r, g, b))
    while b > min_bright:
        if b > min_bright: b -= step
        
        for pos in bluepix:
            pixels[pos] = (r, g, b)
            pixels.show()
            print('(Pixel {}) = (R:{}, G:{}, B:{})'.format(pos, r, g, b))
        time.sleep(delay)

def white_pixels(r = 0, g = 0, b = 0):
    WR = r
    WG = g
    WB = b
    print("Begin - White RGB values are {}/{}/{}".format(WR, WG, WB))        
    while r < max_bright or g < max_bright or b < max_bright:
        if r < max_bright: r += step
        if g < max_bright: g += step
        if b < max_bright: b += step

        for pos in whitepix:
            pixels[pos] = (r, g, b)
            pixels.show()
	   
            print('(Pixel {}) = (R:{}, G:{}, B:{})'.format(pos, r, g, b))
        time.sleep(delay)

        WR = r
        WG = g
        WB = b
    print("Finished - White RGB values are {}/{}/{}".format(WR, WG, WB))
    

def white_pixels_down(r = max_bright, g = max_bright, b = max_bright):
    WR = r
    WG = g
    WB = b
    print("Begin - White RGB values are {}/{}/{}".format(WR, WG, WB))        
    while r > min_bright or g > min_bright or b > min_bright:
        if r > min_bright: r -= step
        if g > min_bright: g -= step
        if b > min_bright: b -= step

        for pos in whitepix:
            pixels[pos] = (r, g, b)
            pixels.show()
	   
            print('(Pixel {}) = (R:{}, G:{}, B:{})'.format(pos, r, g, b))
        time.sleep(delay)

        WR = r
        WG = g
        WB = b
    print("Finished - White RGB values are {}/{}/{}".format(WR, WG, WB)) 

def sunrise():
    blue_pixels()
    red_pixels()
    white_pixels()
    
def sunset():
    red_pixels_down(max_bright)
    white_pixels_down(max_bright, max_bright, max_bright)
    blue_pixels_down(0, 0, max_bright)
    
    
sunrise()
time.sleep(5)
sunset()

    