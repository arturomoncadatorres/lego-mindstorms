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
# # `crazy_shopper`
# Python equivalent of the `Crazy shopper` program. Let's help Charly deliver his shopping!
#
# # Required robot
# * Charlie (with shopping cart)
#
# <img src="./multimedia/charlie_shopper.jpg" width="50%" align="center">
#
# # Source code
# You can find the code in the accompanying [`.py` file](https://github.com/arturomoncadatorres/lego-mindstorms/blob/main/base/charlie/crazy_shopper.py). To get it running, simply copy and paste it in a new Mindstorms project.
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

# %%
hub.status_light.on('black')

# %% [markdown]
# # Configure motors

# %%
print("Configuring motors...")
motors_wheels = MotorPair('A', 'E')
motors_wheels.set_default_speed(70)

motor_left_arm = Motor('B') # Left arm
motor_right_arm = Motor('F') # Right arm

motor_left_arm.set_default_speed(40)
motor_right_arm.set_default_speed(-40)

motors_arms = MotorPair('B', 'F')
print("DONE!")

# %% [markdown]
# # Set arm motors to starting position
# This isn't part of the original program, but I think it is good practice to make sure motors always start in the same state.
#

# %%
print("Setting arm motors to position 0...")
motor_left_arm.run_to_position(0)
motor_right_arm.run_to_position(0)
print("DONE!")

# %% [markdown]
# # Move shopper Charlie
#
# So far, we've used `move` to move the wheel motors. 
# However, when using `move`, the program will not continue until the specified value is reached. 
# This is a problem, since we want to move the wheels *and* the arms at the same time.
# Therefore, we will use `start` and `stop`. This comes at the cost of being unable to
# define a stopping condition based on the motors alone (e.g., distance, time). 
# We have to stop them at certain point of the program (as we do here) or based on a 
# sensory input. 
#
# I wonder if there's a way to perform async execution using the vanilla (Micro)Python.
# I'll look into that in the future.

# %%
print("Moving shopper Charlie...")
motors_wheels.start()
wait_for_seconds(1) # This delays moving the arms, but doesn't affect the already moving wheel motors.

for ii in range(0, 5):
    motors_arms.move(0.3, unit='seconds', speed=40)
    motors_arms.move(0.2, unit='seconds', speed=-40)

motors_wheels.stop()
print("DONE!")

# %%
print("-"*15 + " Execution ended " + "-"*15 + "\n")
"""
