#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (
    Motor,
    TouchSensor,
    ColorSensor,
    InfraredSensor,
    UltrasonicSensor,
    GyroSensor,
)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from time import sleep


# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.

# Initialize a motor at port B.
MotorLinks = Motor(Port.B)
MotorRechts = Motor(Port.D)

base = DriveBase(MotorLinks, MotorRechts, 40, 140)

base.straight(500)

SensorLichtLinks = Sensor(Port.1)
SensorLichtRechts = Sensor(Port.4)

# Run the motor up to 500 degrees per second.
# To a target angle of 90 degrees.
# MotorLinks.run_target(500, 90)
#
# # Create your objects here.
# ev3 = EV3Brick()
#
#
# # Write your program here.
# ev3.speaker.beep()
# sleep(1)
# ev3.speaker.beep()
# ev3.speaker.beep()
# ev3.speaker.beep()
# ev3.speaker.beep()