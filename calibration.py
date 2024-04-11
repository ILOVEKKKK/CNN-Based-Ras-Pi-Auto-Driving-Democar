''' Script for calibrating the Tamiya TBLE-02S ESC to a raspberry pi PWM
'''

import RPi.GPIO as GPIO
import time

def input_check(inp):
    if inp != 'y':
        quit()

try:
    print('Do not switch on the ESC yet! If any part of the calibration fails, switch off the ESC and rerun this script.\n\n1. Connect the ESC Gnd (black) to the Pi Gnd pin\n2. Connect the ESC signal (white) to the Pi #12 pin (DO NOT CONNECT THE ESC RED WIRE TO THE PI)')
    input_check(input('Done? y/n: '))
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(12, GPIO.OUT)
    engine = GPIO.PWM(12, 50)
    engine.start(7.5)
    
    print('3. Switch on the ESC and await a few long beeps, followed by silence\n 4.Hold down the Set button on the ESC, observe changing LED lights (green -> orange -> red -> green -> ...) and release on red')
    input_check(input('Done? y/n: '))
    
    time.sleep(2)
    engine.ChangeDutyCycle(10)
    time.sleep(2)
    
    print('5. Press the set button once and observe a double flashing LED.')
    input_check(input('Done? y/n: '))
    
    time.sleep(2)
    engine.ChangeDutyCycle(5)
    time.sleep(2)
    
    print('6. Press the set button once more. If the LED turns off, calibration is complete.')
    input_check(input('Did the LED turn off? y/n: '))
    
    time.sleep(2)
    engine.ChangeDutyCycle(7.5)
    time.sleep(2)
    
    print('Calibration complete.')
finally:
    engine.ChangeDutyCycle(7.5)
    GPIO.cleanup()
