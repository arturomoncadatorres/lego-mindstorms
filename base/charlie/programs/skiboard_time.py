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
# # `skiboard_time`
# Python equivalent of the `Skiboard time` program. Charlie goes skiing on his board.
#
# # Required robot
# * Charlie (with skiboard and poles)
#
# <img src="../multimedia/charlie_skiboard.jpg" width="50%" align="center">
#
# # Source code
# You can find the code in the accompanying [`.py` file](https://github.com/arturomoncadatorres/lego-mindstorms/blob/main/base/charlie/programs/skiboard_time.py). To get it running, simply copy and paste it in a new Mindstorms project.
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
motor_left_arm = Motor('B') # Left arm
motor_right_arm = Motor('F') # Right arm
motors_arms = MotorPair('B', 'F')

motor_left_arm.set_default_speed(-100)
motor_right_arm.set_default_speed(100)
print("DONE!")

# %% [markdown]
# # Set arm motors to starting position

# %%
print("Setting arm motors to position 0...")
motor_left_arm.run_to_position(0)
motor_right_arm.run_to_position(0)
print("DONE!")


# %% [markdown]
# # Make Charlie push himself around
# If Charlie doesn't move properly, try:
# * adjusting the wheels on his poles
# * playing with the waiting time between movement of the right arm (`t_wait`)
# * putting him on another surface

# %%
print("Skiing...")

# Original value is 6.
# I set this to 3 due to space constraints.
n_pushes = 3

for ii in range(0, n_pushes):

    # Now, we move the arm motors back to position 0 sequentially.
    # This doesn't affect the movement, but looks a bit clumsy.
    # An alternative to this could be using coroutines to 
    # make them run "parallel", as in the drum_solo project.
    motor_left_arm.run_to_position(0, direction='shortest path')
    motor_right_arm.run_to_position(0, direction='shortest path')
    motors_arms.move(85, unit='degrees')

    motor_right_arm.start()
    t_wait = 0.1
    wait_for_seconds(t_wait)
    motor_right_arm.stop()

motor_left_arm.run_to_position(0, direction='shortest path')
motor_right_arm.run_to_position(0, direction='shortest path')

app.play_sound('Skid')

print("DONE!")


# %%
print("-"*15 + " Execution ended " + "-"*15 + "\n")
