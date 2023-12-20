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

    for arg in all_args:
        #print all the keys then : then the values
        print(arg,":",all_args[arg])

	if arg == "axis-0":
	    joy1x = float(all_args[arg])
	if arg == "axis-1":
	    joy1y = float(all_args[arg])
	if arg == "axis-3":
	    joy2x = float(all_args[arg])
    #must return something, doesn't really matter what
    return all_args

    thrust_left = min(1, max(-1, joy1y + joy1x)) * drive_speed
    thrust_right = min(1, max(-1, joy1y - joy1x)) * drive_speed
    thrust_up = joy2y * drive_speed

    set_thruster_speed(0, thrust_left)
    set_thruster_speed(1, thrust_right)
    set_thruster_speed(3, thrust_up)
    set_thruster_speed(4, thrust_up)

#Thruster index 0-3
#Speed -100 to 100
def set_thruster_speed(thruster, speed)
{
    pca.channels[thruster].duty_cycle = int((13.107 * speed) + 4915.125)
}



if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False)