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

# Initialize the two light sensors (use ColorSensor for reflected light values).
# Change Port.S1 / Port.S4 to match your actual sensor ports.
light_left = ColorSensor(Port.S4)
light_right = ColorSensor(Port.S1)

# Initialize a distance sensor (Ultrasonic) on the specified port.
# Change Port.S2 to the actual port your distance sensor is connected to.
distance_sensor = UltrasonicSensor(Port.S2)

# Define a threshold for "dark" vs "bright" (0..100).
# You can adjust this value based on your lighting conditions.
DARK_THRESHOLD = 30

# When distance > DISTANCE_STOP_MM, stop movement.
DISTANCE_STOP_MM = 50  # 10 cm

def is_dark(sensor):
    """Return True when the given sensor sees a dark surface."""
    return sensor.reflection() < DARK_THRESHOLD

# Drive based on light sensor values:
# - If the left sensor sees dark, steer to the right.
# - If the right sensor sees dark, steer to the left.
# - If neither sees dark, drive forward.
# - If both see dark, stop.

DRIVE_SPEED = 500  # mm/s
TURN_SPEED = 100  # positive = turn right, negative = turn left

while True:
    # Stop if the distance sensor sees more than 10 cm.
    # (As requested: stop when distance > 10 cm.)
    if distance_sensor.distance() > DISTANCE_STOP_MM:
        base.stop()
        print("Distance > 10 cm: stopping")
        break

    left_dark = is_dark(light_left)
    right_dark = is_dark(light_right)

    if left_dark and not right_dark:
        # Turn right (avoid dark on the left).
        base.drive(DRIVE_SPEED, TURN_SPEED)
    elif right_dark and not left_dark:
        # Turn left (avoid dark on the right).
        base.drive(DRIVE_SPEED, -TURN_SPEED)
    elif left_dark and right_dark:
        # Both sensors see dark: stop and wait.
        base.stop()
    else:
        # Both sensors see bright: go straight.
        base.drive(DRIVE_SPEED, 0)

    wait(200)



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

