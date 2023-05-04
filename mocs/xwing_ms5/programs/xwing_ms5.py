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
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
#
# <p align="center">
#  <img width="100%" src="../../../multimedia/mindstorms_51515_logo.png">
# </p>
#
# # `xwing_ms5`
# Python program to control the X-Wing MS5 robot.
# The ship will angle along the z-axis depending on the hub's orientation.
#
# It also allows switching [between cruise and attack mode](https://scifi.stackexchange.com/questions/6001/why-do-x-wings-change-wing-configuration). 
# While in the latter, the X-Wing can fire its laser cannons.
#
# (I'm still editing a video showcasing the functionality. On the meantime, 
# scroll down for a couple of GIFS that should give you a good idea of what to 
# expect).
#
# # Required robot
# * X-Wing MS5 (you can find the [instructions for building it here](https://arturomoncadatorres.com/xwing-ms5/))
#
# <img src="../multimedia/xwing_ms5.png" width="50%" align="center">
#
# # Source code
# You can find the code in the accompanying [`.py` file](https://github.com/arturomoncadatorres/lego-mindstorms/blob/main/mocs/aat_ms5/programs/xwing_ms5.py). To get it running, simply copy and paste it in a new Mindstorms project.
#
# # Imports

# %%
from mindstorms import Motor, MotorPair, ColorSensor, DistanceSensor, App
from mindstorms.control import wait_for_seconds, wait_until, Timer
from mindstorms.operator import greater_than, greater_than_or_equal_to, less_than, less_than_or_equal_to, equal_to, not_equal_to
import math

# Since we want to play sounds, we need to do everything through hub.
import hub

# %%
print("-"*15 + " Execution started " + "-"*15 + "\n")


# %% [markdown]
# ## Initialize motors

# %%
# Motor for opening/closing the S-foils (i.e., wings).
motor_wings = Motor('A') 

# Motors for tilting the ship
# Due to the weight of the ship, we need two motors.
motor_b = hub.port.B.motor
motor_d = hub.port.D.motor
motors_base = motor_b.pair(motor_d)


# %% [markdown]
# Notice we initialize the motor to 350 (and not 0) to
# make sure that there's a little bit of tension as the wings
# are closed. Otherwise, the wings are very loose.

# %%
print("Initializing motors to position 0...")
motor_wings.run_to_position(350, direction='shortest path', speed=100)
motors_base.preset(0, 0)
print("DONE!")


# %% [markdown]
# ## Initialize conditions
# `WINGS_CLOSED` will keep track of the state of the wings.

# %%
print("Initializing conditions...")
WINGS_CLOSED = True

# %% [markdown]
# In order to avoid sudden changes in the angle, we will use a simple
# [moving average filter](https://en.wikipedia.org/wiki/Moving_average).
# We will usse a `WINDOW_SIZE` of 3 samples. 
#
# I experimented with different sizes and this one was acceptable in making 
# the movement smoother without making the response sluggish. 
# I think up to 7 or 8 is ok, a window size of more than 10 makes it very slow.

# %%
WINDOW_SIZE = 3

angleB_array = [0.001] * WINDOW_SIZE
angleD_array = [0.001] * WINDOW_SIZE


# %% [markdown]
# We will create some animation frames for displaying the laser on the hub.
# This is pretty much identical to what I used for the
# [AAT MS5](https://github.com/arturomoncadatorres/lego-mindstorms/tree/main/mocs/aat_ms5) robot
# (except it is flipped from top to bottom due to the orientation of the hub).

# %%
# Define animation frames for the laser cannon.
frames = ['00000:00000:00000:00000:00000',
'00000:00000:00000:00000:00500',
'00000:00000:00000:00500:00700',
'00000:00000:00500:00700:00900',
'00000:00500:00700:00900:00000',
'00500:00700:00900:00000:00000',
'00700:00900:00000:00000:00000',
'00900:00000:00000:00000:00000',
'00000:00000:00000:00000:00000']

n_frames = len(frames)
t_pause = 0.05 # Pause between frames (in seconds)

print("DONE!")


# %% [markdown]
# ## Putting the X-Wing MS5 in action!
#
# The way the robot works is as follows:
# * Tilting the hub left to right will make the ship follow accordingly.
#
# <p align="center">
#  <img width="100%" src="../multimedia/tilt.gif">
# </p>
#
# * Pushing the right button locks the S-foils (i.e., the wings) from cruise 
# mode (closed) to attack position (open) and viceversa. 
# * While in attack position, pushing the left button will shoot the laser 
# cannons, showing an animation on the hub. The cannons cannot be fired with 
# the S-foils closed.
#
# <p align="center">
#  <img width="100%" src="../multimedia/sfoil.gif">
# </p>
#
# The program will run indefinitely until stopped manually in the 
# LEGO MINDSTORMS app.

# %%
while True:

    if hub.button.right.was_pressed():
        print("Right button was pressed")

        # If the wings were closed...
        if WINGS_CLOSED == True:
            # ...open them.
            motor_wings.run_to_position(20, direction='shortest path', speed=2)
            WINGS_CLOSED = False
            print("Wings are open!")

        # If the wings were opened...
        elif WINGS_CLOSED == False:
            # ...close them.
            motor_wings.run_to_position(350, direction='shortest path', speed=2)
            WINGS_CLOSED = True
            print("Wings are closed!")


    if hub.button.left.was_pressed():
        print("Left button was pressed")

        # If the wings were closed...
        if WINGS_CLOSED == True:
            print("Can't shoot with S-foils closed!")

        # If the wings were opened...
        elif WINGS_CLOSED == False:
            print("Laser cannons fired!")

            # ...play sound...
            hub.sound.play("/extra_files/Laser")

            # ...and display laser cannon animation.
            for ii in range(0, n_frames):
                img = hub.Image(frames[ii])
                hub.display.show(img)
                wait_for_seconds(t_pause)
            
    
    yaw, pitch, roll = hub.motion.yaw_pitch_roll()

    # We will map the roll from -90 to 90 to a defined range
    # by dividing it by a factor.
    max_angle = 30
    angle_factor = 90/max_angle
    angle = roll/angle_factor
    
    # Notice how we limit the range of the motors movement
    # between -max_angle and max_angle (otherwise the X-Wing tilts too much)
    if angle >= 0:
        angleB = max([-angle, -max_angle])
        angleD = min([angle, max_angle])
    if angle < 0:
        angleB = min([-angle, max_angle])
        angleD = max([angle, -max_angle])
    print("Roll = " + str(roll) + "; max angle = " + str(max_angle) + "; angle = " + str(angle) + "; angleB = " + str(angleB) + "; angleD = " + str(angleD))

    # Update the angle arrays by appending the new sample at the end of
    # the array while popping the first sample.
    angleB_array.append(angleB)
    angleB_array.pop(0)

    angleD_array.append(angleD)
    angleD_array.pop(0)

    # Get the mean of the current window and use it for setting the
    # motor positions.
    angleB_mean = sum(angleB_array)/WINDOW_SIZE
    angleD_mean = sum(angleD_array)/WINDOW_SIZE

    print("Mean of angleB = " + str(angleB_mean) + "; mean of angleD = " + str(angleD_mean))
    motors_base.run_to_position(angleB_mean, angleD_mean, speed=10, max_power=100, stop=2)
    
    
# We will never get here.
print("-"*15 + " Execution ended " + "-"*15 + "\n")
