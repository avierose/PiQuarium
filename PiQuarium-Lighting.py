# Last updated 14/4/2019

import datetime
import time
import board
import neopixel
import RPi.GPIO as GPIO

# User settings
usrDelay = 3  # Delay between each increment in LED lighting change (higher equals longer change times)
softDelay = 0.01
usrStep = 1  # How much to increase the LED lighting at each step (1-255)
usrMaxBright = 255  # Maximum brightness of the LEDs (max 255)
usrMinBright = 0  # Minimum brightness of LEDs (suggested 0, otherwise lights will never be completely off)
usrMoonLight = 55  # How bright the moon lighting should be
usrNumPixels = 54 # Number of pixels in your neo-pixel strip

# Light times
sunriseStart = datetime.time(7, 50, 0)  # Time of sunrise start
softOnStart = datetime.time(10, 50, 0)
sunsetStart = datetime.time(22, 55, 0)  # Time of sunset start
moonStart = datetime.time(0, 36, 0)  # Time of moon set (fade to complete dark)
nightStart = datetime.time(0, 39, 0)  # Time when all lights will be off (suggest allowing 5 mins after moonStart)

# Run Tokens
sunriseRun = False
sunsetRun = False
moonRun = False

# Mode Tokens
GPIO.setwarnings(False)
##GPIO.setmode(GPIO.BOARD)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
OVERRIDE = False

# Neopixel set-up
ORDER = neopixel.GRB
pixelPin = board.D18  # Data pin for neopixels
pixels = neopixel.NeoPixel(pixelPin, usrNumPixels,
                           brightness=1,
                           auto_write=False,
                           pixel_order=ORDER)

redPix = []
bluePix = []
whitePix = []

for pix in range(usrNumPixels):
    if pix % 4 == 0:  # every 4th number from 0
        redPix.append(pix)
    elif pix % 4 == 1:  # every 4th number from 1
        bluePix.append(pix)
    else:  # all other positions in the range
        whitePix.append(pix)


def fade(pixelColour,
         fadeUp,
         maxBrightR,
         minBrightR,
         maxBrightG,
         minBrightG,
         maxBrightB,
         minBrightB,
         r, g, b,
         delay = usrDelay):

    # Catching the pixel colour to alter
    if pixelColour == 'red':
        pixList = redPix
    elif pixelColour == 'blue':
        pixList = bluePix
    elif pixelColour == 'white':
        pixList = whitePix
    else:
        print('No valid pixel colour defined')

    # Catching if fading up or down
    if fadeUp:
        while r < maxBrightR or g < maxBrightG or b < maxBrightB:
            if r < maxBrightR:
                r += 1
            if g < maxBrightG:
                g += 1
            if b < maxBrightB:
                b += 1
            for pos in pixList:
                pixels[pos] = (r, g, b)
                pixels.show()
                print('(Pixel {}) = (R:{}, G:{}, B:{})'.format(pos, r, g, b))
            time.sleep(delay)

    if not fadeUp:
        while r > minBrightR or g > minBrightG or b > minBrightB:
            if r > minBrightR:
                r -= 1
            if g > minBrightG:
                g -= 1
            if b > minBrightB:
                b -= 1

            for pos in pixList:
                pixels[pos] = (r, g, b)
                pixels.show()
                print('(Pixel {}) = (R:{}, G:{}, B:{})'.format(pos, r, g, b))
            time.sleep(delay)


def sunRise():
    print('Starting Sunrise')
    fade('blue', True, usrMinBright, usrMinBright, usrMinBright, usrMinBright, usrMaxBright, usrMinBright,
         usrMinBright, usrMinBright, usrMinBright, usrDelay)
    fade('red', True, usrMaxBright, usrMinBright, usrMinBright, usrMinBright, usrMinBright, usrMinBright,
         usrMinBright, usrMinBright, usrMinBright, usrDelay)
    fade('white', True, usrMaxBright, usrMinBright, usrMaxBright, usrMinBright, usrMaxBright, usrMinBright,
         usrMinBright, usrMinBright, usrMinBright, usrDelay)
    print('Sunrise finished')
    
def softOn():
    print('Starting Soft On')
    fade('blue', True, usrMinBright, usrMinBright, usrMinBright, usrMinBright, usrMaxBright, usrMinBright,
         usrMinBright, usrMinBright, usrMinBright, softDelay)
    fade('red', True, usrMaxBright, usrMinBright, usrMinBright, usrMinBright, usrMinBright, usrMinBright,
         usrMinBright, usrMinBright, usrMinBright, softDelay)
    fade('white', True, usrMaxBright, usrMinBright, usrMaxBright, usrMinBright, usrMaxBright, usrMinBright,
         usrMinBright, usrMinBright, usrMinBright, softDelay)
    print('Soft On finished')


def sunSet():
    print('Starting Sunset')
    fade('white', False, usrMaxBright, usrMinBright, usrMaxBright, usrMinBright, usrMaxBright, usrMinBright,
         usrMaxBright, usrMaxBright, usrMaxBright, usrDelay)
    fade('red', False, usrMaxBright, usrMinBright, usrMinBright, usrMinBright, usrMinBright, usrMinBright,
         usrMaxBright, usrMinBright, usrMinBright, usrDelay)
    fade('blue', False, usrMinBright, usrMinBright, usrMinBright, usrMinBright, usrMaxBright, usrMoonLight,
         usrMinBright, usrMinBright, usrMaxBright, usrDelay)


    print('Sunset Finished')


def moonSet():
    print('Starting Moonset')
    fade('blue', False, usrMinBright, usrMinBright, usrMinBright, usrMinBright, usrMoonLight, usrMinBright,
         usrMinBright, usrMinBright, usrMoonLight, usrDelay)
    print('Moonset Finished')


def isNowInTimePeriod(startTime, endTime, nowTime):
    if startTime < endTime:
        if startTime < nowTime < endTime:
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
        print(timeNow.strftime('%H:%M:%S'), 'Time in range - Starting now')
        return True
    else:
        print(timeNow.strftime('%H:%M:%S'), 'Time not in range - waiting until', timeStart.strftime('%H:%M:%S'))

def toggleOverride():
    if not OVERRIDE:
        OVERRIDE = True
    else:
        OVERRIDE = False
    

# Main loop

while True:
    if GPIO.input(23) == GPIO.HIGH:
        print("Button Pressed")
        toggleOverride()
        if OVERRIDE == True:
            softOn()

    while OVERRIDE == False:
        # Sunrise
        if not sunriseRun:
            if checkTime(sunriseStart, softOnStart):
                sunRise()
                sunriseRun = True
                
        # Soft On
        if not sunriseRun:
            if checkTime(softOnStart, sunsetStart):
                softOn()
                sunriseRun = True

        # Sunset - Hold moon lighting until night
        if not sunsetRun:
            if checkTime(sunsetStart, moonStart):
                sunSet()
                sunsetRun = True

        # Moon sets into darkness
        if not moonRun:
            if checkTime(moonStart, nightStart):
                moonSet()
                moonRun = True

        # Reset run tokens
        if moonRun:
            if checkTime(nightStart, sunriseStart):
                moonRun = False
                sunsetRun = False
                sunriseRun = False
        time.sleep(1)
