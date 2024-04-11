import threading
import inputs #logitech controller read-out
from time import sleep
import requests
import serial
import sys
import picamera
import picamera.array
import PIL
from PIL import Image
import uuid
import csv
import numpy as np

class MotorControllerGPIO:
    def __init__(self):
        self.steering_angle = 0 #initial steering angle [-45, 45]
        self.speed = 0 #intital speed [km/h]
        self.max_steering_angle = 45 #degrees [-45, 45]
        self.manual_drive_speed = 1.5 #km/h
        self.capture_rate = 6 #fps
        self.arduino_serial = serial.Serial('/dev/ttyACM0', 57600, timeout=0.5)
#       self.arduino_serial = serial.Serial('/dev/serial0', 57600, timeout=0.5)
        self.logfile=open("logfile.csv","w+")
        self.logfile.write("sep=,\r\n")
        self.image = np.zeros((48, 64, 3))
        self.camera = picamera.PiCamera()
        self.frame_stream = picamera.array.PiRGBArray(self.camera)
        self.capture_iterator = self.camera.capture_continuous(self.frame_stream, use_video_port=True, format='bgr')
        self.capture_count = 0

    def update_steering(self, target_speed, steering_angle):
        
        #Send acceleration [-100,100] (%) and steering angle [-90,90] (deg) to Arduino UNO motor controller via serial port
        #Format: speed,steering_angle

        steering_angle = steering_angle+90
        #print(acceleration)
        #print(steering_angle)
        speed_round=round(float(target_speed),2)
        steering_round=round(float(steering_angle),2)
        check_round=round(speed_round+steering_round,2)
        serial_string= '#' + str(speed_round) + ',' + str(steering_round) + ',' + str(check_round) + '*'
        #serial_string = str(round(float(target_speed),3)) + ',' + str(int(steering_angle)) + '^'
        #print(serial_string)
        for c in list(serial_string):
            #print(c)
            self.arduino_serial.write(c.encode())
        if self.arduino_serial.in_waiting:
            arduinoData=self.arduino_serial.readline().decode('latin-1', errors="replace")
            self.logfile.write(arduinoData)

    def capture_thread(self):
        while True:
            sleep(1/self.capture_rate)
            if self.speed > 0:
                self.image = next(self.capture_iterator).array
                self.frame_stream.seek(0)
                PILimage = Image.fromarray(self.image)
                image_fname = uuid.uuid4().hex + ".jpg"
                PILimage.save("training_data/" + image_fname)
                data = [image_fname, self.steering_angle]
                with open(r"training_data/train.csv", "a") as f:
                    wrt = csv.writer(f, lineterminator="\n")
                    wrt.writerow(data)
                self.capture_count += 1
                print('number of training images: ', self.capture_count)

    def manual_drive(self):
        '''
        Drive car with bluetooth controller
        '''
        print('booting up')
        cpt_thread = threading.Thread(target=self.capture_thread, args=())
        cpt_thread.daemon = True
        cpt_thread.start()
        sleep(2)
        print('ready to drive')

        while True:
            events = inputs.get_gamepad()
            for event in events:
                #print(event.code)
                #print(event.state)
                if event.code == 'ABS_Y':
                    if event.state == -32768:
                        self.speed = self.manual_drive_speed
                    else:
                        self.speed = 0
                if event.code == 'ABS_RX':
                    self.steering_angle = -self.max_steering_angle * event.state / 32767.
                self.update_steering(self.speed, self.steering_angle)

            # stop program once 500 training images have been recorded
            if self.capture_count > 500:
                print("500 training images have been recorded.")
                quit()


class MotorController():
    def __init__(self):
        self.controller = MotorControllerGPIO()
        

    def __enter__(self):
        return self.controller

    def __exit__(self, type, value, traceback):
        self.controller.update_steering(0, 0)
        print('Stopping. Steering straight.')
        self.controller.logfile.write("Closing the file...\n")
        self.controller.logfile.close()
        print("Writing to logfile")
        sleep(0.5)
        print("Exit")

def main():
    with MotorController() as controller:
        controller.manual_drive()

if __name__ == "__main__":
    main()
