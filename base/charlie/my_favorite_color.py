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
# # `my_favorite_color`
# Python equivalent of the `My favorite color` program. Makes Charlie react differently depending on the color we show him.
#
# # Required robot
# * Charlie (with color sensor and color palette)
#
# <img src="./multimedia/charlie_color.jpg" width="50%" align="center">
#
# # Source code
# You can find the code in the accompanying [`.py` file](https://github.com/arturomoncadatorres/lego-mindstorms/blob/main/base/charlie/my_favorite_color.py). To get it running, simply copy and paste it in a new Mindstorms project.
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
motors_movement = MotorPair('A', 'E')
motors_movement.set_default_speed(80)
print("DONE!")

# %% [markdown]
# # Program color reactions

# %%
color_sensor = ColorSensor('C')

# %% [markdown]
# We will use a counter to control printing on the console.
# First, we need to initialize it.

# %%
ii = 0

# %% [markdown]
# Execution

# %%
while True: # This will make the execution go forever

    if ii == 0:
        # We will only print "Waiting for color" when the counter is 0.
        print("Waiting for color...")
    
    # Get the color value.
    color = color_sensor.get_color()

    # We need to make sure that Charlie reacts only when he perceives a color.
    # To do so, we check what color Charlie perceived. If he didn't perceive
    # a color, color_sensor.get_color() returns None.
    if not color == None:

        print("Reacting to color " + color + "...")
        
        # Turn on the center button of the corresponding color.
        hub.status_light.on(color)

        # Let's give it a short pause.
        wait_for_seconds(1)

        # Define reactions to each color.
        if color == 'green':
            hub.light_matrix.show_image('HAPPY')
            motors_movement.move(40, unit='cm', steering=100)
            motors_movement.move(40, unit='cm', steering=-100)

        elif color == 'yellow':
            hub.light_matrix.show_image('SURPRISED')
            motors_movement.move(-20, unit='cm', steering=0)

        elif color == 'red':
            hub.light_matrix.show_image('ANGRY')
            motors_movement.move(10, unit='cm', steering=0)

        else:
            # For all the other colors, do nothing.
            # If we want a program to do nothing, we can use pass.
            # Just for the sake of demonstration/completion. 
            pass

        # Turn off center button and image.
        hub.status_light.on('black')
        hub.light_matrix.off()
        
        print("DONE!")
        
        # Reset the counter to 0, to make sure that "Waiting for color" is printed (again).
        ii = 0        


    else:
        # If no color was perceived, increase the counter.
        # This way, we make sure that the "Waiting for color" text is printed on the console
        # just once (when it has a value of 0). Otherwise, it would be printed continuously every time the sensor got its reading.

        ii = ii + 1 # Alternatively, we could've written ii =+ 1, which is a bit shorter (and very common in Python).

# %% [markdown]
# Notice, though, how we will never reach the following line, since the execution of the program is in a `while True`.

# %%
print("-"*15 + " Execution ended " + "-"*15 + "\n")
