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
# # `high_five`
# Python equivalent of the `High five!` program. Let's high five our favorite robot. Don't let him hanging!
#
# # Required robot
# * Charlie (with distance sensor)
#
# <img src="../multimedia/charlie_distance.png" width="50%" align="center">
#
# # Source code
# You can find the code in the accompanying [`.py` file](https://github.com/arturomoncadatorres/lego-mindstorms/blob/main/base/charlie/programs/high_five.py). To get it running, simply copy and paste it in a new Mindstorms project.
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
motors_wheels = MotorPair('A', 'E')
print("DONE!")

# %% [markdown]
# # Set arm motors to starting position

# %%
print("Setting arm motors to position 0...")
motor_left_arm.run_to_position(0)
motor_right_arm.run_to_position(0)
print("DONE!")

# %% [markdown]
# # Configure sensor

# %%
print("Configuring distance sensor...")
distance_sensor = DistanceSensor('D')
distance_sensor.light_up_all()
print("DONE!")

# %% [markdown]
# # High five!

# %%
print("Waiting for high five intention...")
distance_sensor.wait_for_distance_closer_than(12, unit='cm')
distance_sensor.light_up_all(0)
print("DONE!")

# %%
print("Let's high five!")
motor_right_arm.run_for_degrees(-120)

timer = Timer()

def high_five_or_no_high_five():
    # Original threshold of speed is -10.
    # However, in my experience, -5 worked better.
    return (motor_right_arm.get_speed() < -5) or (timer.now() > 5)

# Wait for either a high five or for the timer to go past 5 s.
wait_until(high_five_or_no_high_five)

# If the timer exceeded 5, it means that there was no high five.
if timer.now() > 5:
    print("No high five :( ")
    hub.light_matrix.show_image('SAD')
    app.play_sound('Lose')
    motor_right_arm.run_to_position(0, direction='shortest path')
    motors_wheels.move(-20, unit='cm')

# Otherwise, it means that there was a high five.
else:
    print("High five :) ")
    hub.light_matrix.show_image('HAPPY')
    app.play_sound('Crazy Laugh')
    motor_right_arm.run_to_position(0, direction='shortest path')

# %%
print("-"*15 + " Execution ended " + "-"*15 + "\n")
