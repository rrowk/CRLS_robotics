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


app = flask.Flask("RobotServer")
@app.route("/")
# gpio.setmode(gpio.BOARD)
# gpio.setup(37,)

def send():
    #turn the url queries into a dictionary
    os.system('clear')
    all_args = flask.request.args.to_dict()
    time.sleep(0.1)
    for arg in all_args:
        #print all the keys then : then the values
        print(arg,":",all_args[arg])
    #must return something, doesn't really matter what
    return all_args

#Thruster index 0-3
#Speed -100 to 100
def set_thruster_speed(thruster, speed)
{
    frequency = 50
    pulse_length = 1500 + (4 * speed)
    pca.channels[thruster].duty_cycle = 65536((20000)/pulse_length) - 1

}



if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False)

print("Setup Complete :)")