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
# # `shy_guy`
# Python equivalent of the `Shy guy` program. Charlie can be quite shy sometimes!
#
# # Required robot
# * Charlie (with distance sensor)
#
# <img src="../multimedia/charlie_distance.png" width="50%" align="center">
#
# # Source code
# You can find the code in the accompanying [`.py` file](https://github.com/arturomoncadatorres/lego-mindstorms/blob/main/base/charlie/programs/shy_guy.py). To get it running, simply copy and paste it in a new Mindstorms project.
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
hub.light_matrix.show_image('SILLY')


# %% [markdown]
# # Configure motors

# %%
print("Configuring motors...")
motors_wheels = MotorPair('A', 'E')
motors_wheels.set_default_speed(80)

motor_left_arm = Motor('B') # Left arm
motor_right_arm = Motor('F') # Right arm

motor_left_arm.set_default_speed(75)
motor_right_arm.set_default_speed(-75)

motors_arms = MotorPair('B', 'F')
print("DONE!")

# %% [markdown]
# # Set arm motors to starting position

# %%
print("Setting arm motors to position 0...")
motor_left_arm.run_to_position(0)
motor_right_arm.run_to_position(0)
print("DONE!")

# %% [markdown]
# # Make Charlie shy

# %%
# Initialize the distance sensor.
print("Initializing the distance sensor...")
distance_sensor = DistanceSensor('D')
print("DONE!")

# %%
# Turn on the lights of the distance sensor.
print("Turning on the distance sensor...")
distance_sensor.light_up_all(100)
print("DONE!")

# %% [markdown]
# Define Charlie's shy reaction.

# %%
while True:

    # Get distance measurement.
    distance = distance_sensor.get_distance_cm()
    print("Distance measurement: " + str(distance) + " cm")

    # We need to make sure that Charlie reacts only when he perceives a distance.
    # To do so, we check what distance Charlie perceived. If he didn't perceive
    # a distance, distance_sensor.get_distance_cm() returns None.
    if not distance == None:

        # Charlie will get embarrassed if you get closer than 30 cm
        # For now, I defined this distance as 15 cm for testing purposes.
        distance_threshold = 15
        if distance < distance_threshold:

            print("Charlie is embarrassed! (distance = " + str(distance) + " cm)")

            # Turn off the lights of the distance sensor.
            print("Turning off the distance sensor...")
            distance_sensor.light_up_all(0)
            print("DONE!")

            # Charlie runs away out of shyness.
            print("Charlie is running away!")        
            hub.light_matrix.show_image('CONFUSED')
            app.start_sound('Cuckoo')

            
            motors_arms.move(-90, unit='degrees')

            motors_wheels.move(-15, unit='cm')
            motors_wheels.move(20, unit='cm', steering=100)

            app.start_sound('Cuckoo')

            motors_wheels.move(30, unit='cm')
            motors_wheels.move(20, unit='cm', steering=100)

            app.start_sound('Cuckoo')

            motors_arms.move(90, unit='degrees')
            print("DONE!")

        print("Turning on the distance sensor (again)...")
        distance_sensor.light_up_all()
        print("DONE!")


# %% [markdown]
# Notice, though, how we will never reach the following line, since the execution of the program is in a `while True`.

# %%
print("-"*15 + " Execution ended " + "-"*15 + "\n")
