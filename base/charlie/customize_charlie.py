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
# # `customize_charlie`
# Python equivalent of the `Customize Charlie` program. Play with Charlie and make him discover the world around him.
#
# # Required robot
# * Charlie
#
# <img src="./multimedia/charlie.png" width="50%" align="center">
#
# # Source code
# You can find the code in the accompanying [`.py` file](https://github.com/arturomoncadatorres/lego-mindstorms/blob/main/base/charlie/customize_charlie.py). To get it running, simply copy and paste it in a new Mindstorms project.
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
# # Turn off center button 
# By setting its color to black

# %%
print("Turning center button off...")
hub.status_light.on('black')
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
# # Configure motors

# %%
print("Configuring motors...")
motors_wheels = MotorPair('A', 'E')
print("DONE!")


# %% [markdown]
# # Rise arms

# %%
print("Rising arms...")
motor_f.set_default_speed(-75)
motors_arms = MotorPair('B', 'F')
motors_arms.move(-90, unit='degrees') # Negative angle is clockwise movement
motors_arms.move(90, unit='degrees') # Positive angle is counterclockwise movement
print("DONE!")


# %% [markdown]
# # Customizing Charlie
# ## Defining functions
# I think that the main point of the original program is to show how Scratch's `My Block`s work.
# This is the equivalent of Python functions. Thus, first we will define them.
#
# It is important to note how the objects `hue`, `app`, and all the motors are defined globally
# (and don't need to be passed as arguments to the functions). It is also worth mentioning that
# it is good practice that functions always return something, even if it is a `None`.

# %%
def charlie_happy():
    print("Making Charlie happy...")

    hub.light_matrix.show_image('HAPPY')
    app.start_sound('Robot 1')

    # Move forward.
    motors_wheels.move(10, steering=0)

    # Move arms.
    motor_f.run_for_degrees(90)
    for ii in range(0,3):
        motor_f.run_for_seconds(0.2, speed=100)
        motor_f.run_for_seconds(0.2, speed=-100)
    motor_f.run_to_position(0, direction='shortest path')

    return None

# %%
def charlie_silly():
    print("Making Charlie silly...")

    hub.light_matrix.show_image('SILLY')
    app.start_sound('Robot 2')

    # Turn.
    motors_wheels.move(10, unit='cm', steering=100)

    # Move arms.
    for ii in range(0, 2):
        motor_b.run_to_position(90, direction='clockwise')
        motor_b.run_to_position(270, direction='counterclockwise')
    motor_b.run_to_position(0, direction='shortest path')

    return None

# %%
def charlie_scared():
    print("Making Charlie scared...")

    hub.light_matrix.show_image('CONFUSED') # We have no SCARED image.
    app.start_sound('Robot 3')

    motors_arms.move(-90, unit='degrees', steering=0) # Raise arms
    motors_wheels.move(5, unit='cm', steering=-100) # Turn back
    motors_arms.move(90, unit='degrees', steering=0) # Lower arms
    return None

# %% [markdown]
# ## Execution functions
# Now we can call the functions

# %%
print("Should we make Charlie happy?")
charlie_happy()
wait_for_seconds(2)
print("DONE!")

print("Should we make Charlie silly?")
charlie_silly()
wait_for_seconds(2)
print("DONE!")

print("Should we make Charlie scared?")
charlie_scared()
wait_for_seconds(2)
print("DONE!")

# %%
print("-"*15 + " Execution ended " + "-"*15 + "\n")
