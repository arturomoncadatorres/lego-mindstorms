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
#
# <p align="center">
#  <img width="100%" src="../../multimedia/mindstorms_51515_logo.png">
# </p>
#
# # `time_to_celebrate`
# Python equivalent of the `Time to celebrate` program. Makes Charlie dance.
#
# # Required robot
# * Charlie
#
# <img src="./multimedia/charlie.png" width="50%" align="center">
#
# # Source code
# You can find the code in the accompanying [`.py` file](https://github.com/arturomoncadatorres/lego-mindstorms/blob/main/base/charlie/time_to_celebrate.py). To get it running, simply copy and paste it in a new Mindstorms project.
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
hub = MSHub()
app = App()

# %%
print("-"*15 + " Execution started " + "-"*15 + "\n")

# %% [markdown]
# # Turn off center button 
# By setting its color to black

# %%
print("Turning center button off...")
hub.status_light.on('black')
print("DONE!")

# %% [markdown]
# # Display (happy) image

# %%
print("Displaying happy face...")
hub.light_matrix.show_image('HAPPY')
print("DONE!")


# %% [markdown]
# # Set arm motors to starting position
# In the original Scratch program, there's a `Charlie - Calibrate` block. I don't know exactly how the calibration is done, but in the end I think that it just sets the motor to position 0.
# Notice that moving motors to a specific position needs to be done individually (and sequentially). In other words, we cannot run a `MotorPair` to a position, only one motor at a time.
#

# %%
print("Setting arm motors to position 0...")
motor_b = Motor('B') # Left arm
motor_f = Motor('F') # Right arm
motor_b.run_to_position(0)
motor_f.run_to_position(0)
print("DONE!")

# %% [markdown]
# # Dance time!

# %%
print("Dancing steps 1...")

app.start_sound('Party Blower')

for ii in range(0,2):
    motor_f.run_for_degrees(-100)
    motor_f.run_for_degrees(100)

    motor_b.run_for_degrees(100)
    motor_b.run_for_degrees(-100)
    
print("DONE!")


# %%
print("Dancing steps 2...")

app.start_sound('Party Blower')

motors_af = MotorPair('A', 'F')
motors_be = MotorPair('B', 'E')


for ii in range(0,2):

    motors_af.move(-100, unit='degrees', steering=-100)
    motors_af.move(100, unit='degrees', steering=-100)

    motors_be.move(100, unit='degrees', steering=-100)
    motors_be.move(-100, unit='degrees', steering=-100)

print("DONE!")


# %%
print("Dancing steps 3...")

motors_motion = MotorPair('A', 'E')

motors_motion.move(40, unit='cm', steering=100)
motors_motion.move(40, unit='cm', steering=-100)

# Open hatch
motor_f.run_to_position(270, direction='counterclockwise')
wait_for_seconds(1)
motor_f.run_for_seconds(1)

app.play_sound('Tada')

motor_f.run_to_position(0, direction='counterclockwise')

print("DONE!")


# %%
print("-"*15 + " Execution ended " + "-"*15 + "\n")
