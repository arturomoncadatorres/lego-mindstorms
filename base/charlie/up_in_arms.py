# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.8.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # `up_in_arms`
# Python equivalent of the `Up in arms` program. Charlie waits to be tapped. When tapped, he raises his hands, says hi, and lowers his hands.
#
# # Required robot
# * Charlie
#
# <img src="./multimedia/charlie.png" width="50%" align="center">
#
# # Source code
# You can find the code in the accompanying [`.py` file](https://github.com/arturomoncadatorres/lego-mindstorms/blob/main/base/charlie/up_in_arms.py). To get it running, simply copy and paste it in a new Mindstorms project.
#
# # Imports

# %%
from mindstorms import MSHub, Motor, MotorPair, ColorSensor, DistanceSensor, App
from mindstorms.control import wait_for_seconds, wait_until, Timer
from mindstorms.operator import greater_than, greater_than_or_equal_to, less_than, less_than_or_equal_to, equal_to, not_equal_to
import math

# %% [markdown]
# # Initialization

# %%
print("-"*15 + " Execution started " + "-"*15 + "\n")

# %%
hub = MSHub()
app = App()

# %% [markdown]
# # Start hue
# By turning its button off (i.e., setting its color to black) and displaying the asleep image

# %%
print("Turning center button off...")
hub.status_light.on('black')
print("DONE!")

# %%
print("Displaying asleep face...")
hub.light_matrix.show_image('ASLEEP')
print("DONE!")

# %% [markdown]
# # Set motors to starting position
# In the original Scratch program, there's a `Charlie - Calibrate` block. I don't know exactly how the calibration is done, but in the end I think that it just sets the motor to position 0.
# Notice that moving motors to a specific position needs to be done individually (and sequentially). In other words, we cannot run a `MotorPair` to a position, only a single motor.
#

# %%
print("Setting motors to position 0...")
motor_b = Motor('B')
motor_f = Motor('F')
motor_b.run_to_position(0)
motor_f.run_to_position(0)
print("DONE!")

# %% [markdown]
# # Raise hands when tapped
# All through the execution, we will put pauses on different points to be able to see better what Charlie is doing.

# %%
print("Waiting to be tapped...")

if hub.motion_sensor.wait_for_new_gesture() == 'tapped':
    print("TAPPED!")

    print("Displaying surprised face...")
    hub.light_matrix.show_image('SURPRISED')
    print("DONE!")

    wait_for_seconds(1)

    print("Raise hands...")
    motor_pair = MotorPair('B', 'F')
    motor_pair.set_default_speed(50)
    motor_pair.move(-90, unit='degrees') # Negative angle raises the hands.
    print("DONE!")

    print("Saying 'Hi!'...")
    app.play_sound('Robot 2', 75)
    print("DONE!")

    wait_for_seconds(1)

    print("Lower hands...")
    motor_pair.move(90, unit='degrees') # Positive angle lowers the hands.
    print("DONE!")

    wait_for_seconds(1)

    print("Displaying happy face...")
    hub.light_matrix.show_image('HAPPY')
    print("DONE!")

# %%
print("-"*15 + " Execution ended " + "-"*15 + "\n")
