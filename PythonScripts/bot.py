from flask import Flask, jsonify, request, render_template
import serial
import os
import time
from adafruit_pca9685 import PCA9685
import busio
from board import SCL, SDA
i2c_bus = busio.I2C(SCL, SDA)
pca = PCA9685(i2c_bus)
pca.frequency = 50

drive_speed = 25


app = flask.Flask("RobotServer")
@app.route("/")
# gpio.setmode(gpio.BOARD)
# gpio.setup(37,)

def send():
    #turn the url queries into a dictionary
    os.system('clear')
    all_args = flask.request.args.to_dict()
    time.sleep(0.1)
    joy1x = 0
    joy1y = 0
    joy2y = 0
    trigger = -1
    bumper_left = False
    bumper_right = False

    for arg in all_args:
        #print all the keys then : then the values
        print(arg,":",all_args[arg])

        if arg == "axis-0":
            joy1x = round(float(all_args[arg]), 3)
        if arg == "axis-1":
            joy1y = round(float(all_args[arg]), 3)
        if arg == "axis-4":
            joy2x = round(float(all_args[arg]), 3)
        if arg == "axis-5":
            trigger = round(float(all_args[arg]), 3)
        if arg == "button-4":
            if all_args[arg] == "True":
                bumper_left = True
            else:
                bumper_left = False
        if arg == "button-5":
            if all_args[arg] == "True":
                bumper_right = True
            else:
                bumper_right = False
    #must return something, doesn't really matter what
    drive_percent = drive_speed * ((trigger * 0.5) + 1.5)
    if bumper_left:
        drive_percent = 5
    if bumper_right:
        drive_percent = 60
	
    thrust_left = min(1, max(-1, joy1y + joy1x)) * drive_percent
    thrust_right = min(1, max(-1, joy1y - joy1x)) * drive_percent
    thrust_up = joy2y * drive_speed

    set_thruster_speed(0, thrust_left)
    set_thruster_speed(1, thrust_right)
    set_thruster_speed(3, thrust_up)
    set_thruster_speed(4, thrust_up)
    return all_args

#Thruster index 0-3
#Speed -100 to 100
def set_thruster_speed(thruster, speed):
    capped_speed = min(100, max(-100, speed))
    pca.channels[thruster].duty_cycle = int((13.107 * capped_speed) + 4915.125)



if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False)