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
# # `surprise`
# Python equivalent of the `Surprise!` program. If you show roaming Charlie his favorite color, he will give you a surprise!
#
# # Required robot
# * Charlie (with color *and* distance sensor, as well as his buddies)
#
# <img src="../multimedia/charlie_surprise.jpg" width="50%" align="center">
#
# # Source code
# You can find the code in the accompanying [`.py` file](https://github.com/arturomoncadatorres/lego-mindstorms/blob/main/base/charlie/programs/surprise.py). To get it running, simply copy and paste it in a new Mindstorms project.
#
# # Imports

# %%
from mindstorms import MSHub, Motor, MotorPair, ColorSensor, DistanceSensor, App
from mindstorms.control import wait_for_seconds, wait_until, Timer
from mindstorms.operator import greater_than, greater_than_or_equal_to, less_than, less_than_or_equal_to, equal_to, not_equal_to
import math

# %%
import random # Needed to generate random numbers

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
print("Configuring sensors...")
color_sensor = ColorSensor('C')

distance_sensor = DistanceSensor('D')
distance_sensor.light_up_all()
print("DONE!")


# %% [markdown]
# # Make Charlie roam around

# %%
print("Roaming...")

# While testing, it can be quite annoying having Charlie moving around.
# If you wish, you can just comment the following line. This way,
# Charlie will stay still while you test your program.
motors_wheels.start()


# %% [markdown]
# # Define distance function
# As part of the program, we need to continuously check if the
# measured distance is less than 25 cm. However, if the
# sensor reads no measure, it will return a `None`, which
# in turn will generate an error (since we cannot do a comparision
# between a `None` and something else).
#
# To solve this, we will define our own cuestom distance function.
# This way, when the sensor has no reading, we will just return
# a (simulated) very long distance (instead of returning a `None`).
# This will allow us to do the comparision.

# %%
def my_get_distance_cm():
    """
    Parameters
    ----------
    None
        
    Returns
    -------
    dist:
        Distance value (in cm).
        If the sensor returns a None, it returns a very large value (1000).
    """
    distance = distance_sensor.get_distance_cm()
    if distance == None:
        distance = 1000
        
    return distance

# %% [markdown]
# We can now move on with the rest of the program
#
# # Check for sensor inputs
# We need to constantly check for two conditions: 
# the color and the distance. The original Scratch program
# uses a `wait_until` block. However, doing so blocks checking
# all other inputs. Thus, we will do the implementation here slightly different.


# %%
while True:

    # Check for color.
    color = color_sensor.get_color()
    if color == 'red':
        print('Red color detected!')

        # This break will get us out of the while loop.
        break

    # Check for distance.
    distance = my_get_distance_cm()
    if distance < 25:
        print("Distance sensor triggered!")

        print("Generating random number...")
        random_number = random.randint(1, 3)
        print("Randon number = " + str(random_number) + ". Turning...")

        # Define behaviour of each random number.
        if random_number == 1:
            motors_wheels.move(10, unit='cm', steering=100)
        elif random_number == 2:
            motors_wheels.move(10, unit='cm', steering=-100)
        elif random_number == 3:
            motors_wheels.move(20, unit='cm', steering=100)

        else:
            # It is good practice to cover all possible cases.
            # Here, we make sure that if the generated random number
            # wasn't expected, we send a notification to the user.
            # With the current program, we should never reach this case.
            print("Invalid randon number. Doing nothing.")

        print("DONE!")


# %% [markdown]
# # Make Charlie respond to color
# If red was detected, we get out of the while loop and execute the following code.
# In other words, this is Charlie's response to the color.

# %%
# Stop movement.
motors_wheels.stop()

# %%
hub.light_matrix.show_image('HAPPY')
app.play_sound('Doorbell 1')

# %%
# Open and close Charlie's hatch.
motor_right_arm.run_for_seconds(1)
wait_for_seconds(3)
app.play_sound('Tada')
motor_right_arm.run_to_position(0, direction='counterclockwise')
wait_for_seconds(3)

# %%
# Turn off everything.
distance_sensor.light_up_all(0)
color_sensor.light_up_all(0)

# %%
print("-"*15 + " Execution ended " + "-"*15 + "\n")
