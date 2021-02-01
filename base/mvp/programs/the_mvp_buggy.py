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
# # `the_mvp_buggy`
# Python equivalent of the `The MVP Buggy` program. Make MVP Buggy go round.
#
# # Required robot
# * MVP (in its buggy form)
#
# <img src="../multimedia/mvp_buggy.jpg" width="50%" align="center">
#
# # Source code
# You can find the code in the accompanying [`.py` file](https://github.com/arturomoncadatorres/lego-mindstorms/blob/main/base/mvp/programs/the_mvp_buggy.py). To get it running, simply copy and paste it in a new Mindstorms project.
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

# %%
hub.status_light.on('black')

# %% [markdown]
# # Configure motors

# %%
print("Configuring motors...")
motor_steer = Motor('A') # Front wheels (for steering)
motor_power = Motor('B') # Back wheels (for moving)
print("DONE!")

# %% [markdown]
# # Set steering motor to starting position

# %%
print("Setting steering motor to position 0...")
motor_steer.run_to_position(45, speed=100)
motor_steer.run_to_position(0, speed=100)
print("DONE!")

# %% [markdown]
# # Move MVP

# %%
print("Steering...")
motor_steer.run_to_position(50, speed=35)
print("DONE!")

# %%
print("Moving...")
motor_power.set_default_speed(80)
motor_power.run_for_rotations(-16)
print("DONE!")

# %%
print("-"*15 + " Execution ended " + "-"*15 + "\n")
