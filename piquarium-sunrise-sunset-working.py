import time
import datetime
import board
import neopixel

# Params
pixel_pin = board.D18 # Data pin for neopixels
num_pixels = 30 # Number of pixels
max_bright = 255 # Maximum brightness level
moon_bright = 25 # Brightness level of moonlight
min_bright = 0 # Minimum brightness level
step = 1 # Steps to increase lighting by on each cycle
delay = 1.5 # Delay between cycles in seconds

#Light times
sunriseStart = datetime.time(7, 0, 0)
sunsetStart = datetime.time(21, 30, 0)
moonStart = datetime.time(1, 30, 0)
nightStart = datetime.time(1, 31, 0)

#Booleans
sunriseRun = False
sunsetRun = False
moonRun = False

#Colour Values
global WR
global WG
global WB

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
    while r > min_bright or g > min_bright or b > moon_bright:
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

def isNowInTimePeriod(startTime, endTime, nowTime):
    if startTime < endTime:
        if nowTime > startTime and nowTime < endTime:
            return True
        else:
            return False
    else:
        if nowTime < endTime or nowTime > startTime:
            return True
        else:
            return False
        
def checkTime(start, end):
    timeStart = start 
    timeEnd = end 
    timeNow = datetime.datetime.now().time()
    if isNowInTimePeriod(timeStart, timeEnd, timeNow):
        print(timeNow, "Time in range - Starting now")
        return True
    else:
        print(timeNow, "Time not in range - waiting until", timeStart)
        
def sunrise():
    blue_pixels()
    red_pixels()
    white_pixels()

    
def sunset():
    red_pixels_down(max_bright)
    white_pixels_down(max_bright, max_bright, max_bright)
    blue_pixels_down(0, 0, max_bright)
    
def moonset():
    blue_pixels_down(0, 0, moon_bright)
    
while True:
    #Sunrise
    if sunriseRun != True:
        if checkTime(sunriseStart, sunsetStart):
            sunrise()
            sunriseRun = True
        time.sleep(1)
    #Sunset - Hold moon lighting until night    
    if sunsetRun != True:
        if checkTime(sunsetStart, moonStart):
            sunset()
            sunsetRun = True
        time.sleep(1)
    #Moon sets into darkness    
    if moonRun != True:
        if checkTime(moonStart, nightStart):
            moonset()
            moonRun = True
        time.sleep(1) 
    #reset runs
    if moonRun = True:
        if checkTime(nightStart, sunriseStart):
            moonRun = False
            sunsetRun = False
            sunriseRun = False
        time.sleep(1)

    