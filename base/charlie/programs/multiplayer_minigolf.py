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
#  <img width="100%" src="../../../multimedia/mindstorms_51515_logo.png">
# </p>
#
# # `multiplayer_minigolf`
# Python equivalent of the `Multiplayer mini-golf` program. Take turns to help Charlie score!
#
# # Required robot
# * Charlie (with mini-golf set)
#
# <img src="../multimedia/charlie_minigolf.jpg" width="50%" align="center">
#
# # Source code
# You can find the code in the accompanying [`.py` file](https://github.com/arturomoncadatorres/lego-mindstorms/blob/main/base/charlie/programs/multiplayer_minigolf.py). To get it running, simply copy and paste it in a new Mindstorms project.
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
motor_wheel = Motor('E') # Wheel (for turning around)
motor_left_arm = Motor('B') # Left arm
motor_left_arm.set_default_speed(-80)
print("DONE!")

# %%
print("Setting arm motor to initial position...")
motor_left_arm.run_for_seconds(1)
print("DONE!")

# %% [markdown]
# # Configure sensor

# %%
print("Configuring color sensor...")
color_sensor = ColorSensor('C')
print("DONE!")

# %% [markdown]
# # Hit ball

# %%
while(True):

    print("Waiting for color confirmation...")
    wait_until(color_sensor.get_color, equal_to, 'red')
    print("DONE!")

    print("Hitting ball...")
    motor_left_arm.run_for_degrees(-235)
    motor_left_arm.run_for_seconds(1)

    hub.light_matrix.show_image('HAPPY')
    motor_wheel.run_for_degrees(880) # We can change this value to adjust for turn between shots.
    hub.light_matrix.off()
    
    print("DONE!")


# %% [markdown]
# Notice that since hitting the ball activity is inside an infinite loop,
# we will never reach the following line.

# %%
print("-"*15 + " Execution ended " + "-"*15 + "\n")
