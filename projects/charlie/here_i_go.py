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

# %%
from mindstorms import MSHub, Motor, MotorPair, ColorSensor, DistanceSensor, App
from mindstorms.control import wait_for_seconds, wait_until, Timer
from mindstorms.operator import greater_than, greater_than_or_equal_to, less_than, less_than_or_equal_to, equal_to, not_equal_to
import math

#%% [markdown]
# # Initialization.

#%%
hub = MSHub()
app = App()

#%% [markdown]
# # Set color of center button

#%%
button_color = 'black'
print("Turning color of center button to " + button_color + "...")
hub.status_light.on(button_color)
print("DONE!")

#%% [markdown]
# # Show animation (i.e., image) in hub.

#%%
print("Displaying first image...")
hub.light_matrix.show_image('HAPPY')
print("DONE!")

#%% [markdown]

# # Control motors
# We could initialize and control the motors individually.
# However, it can be very practical to pair them, which can be done as follows.

#%%
# Initialize motors.
print("Initializing motors...")
motor_pair = MotorPair('A', 'E')
print("DONE!")

# Set default speed.
speed = 80
print("Setting default speed to " + str(speed) + "...")
motor_pair.set_default_speed(speed)
print("DONE!")

# Move the motors.
amount = 40

# With steering, we can make the robot turn right (100), 
# turn left (-100) or go straight (0)
steering = 100

print("Moving the motors by " + str(amount) + " cm and steering of " + str(steering) + "...")
motor_pair.move(amount, unit='cm', steering=steering)
print("DONE!")

#%% [markdown]
# # Show animation (i.e., image) in hub.

#%%
print("Displaying last image...")
hub.light_matrix.show_image('CONFUSED')
print("DONE!")

#%% [markdown]
# # Play sound

#%%
sound = 'Wobble'
volume = 75

print("Playing sound '" + sound + "' with volume " + str(volume) + "...")
app.play_sound(sound, volume)
print("DONE!")
