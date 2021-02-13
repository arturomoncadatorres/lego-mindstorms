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
# # `hub_image_animation`
# Small demo of how to display an image and an animation using the hub LEDs.
#
# # Required robot
# * Hub
#
# <img src="../multimedia/hub.jpg" width="50%" align="center">
#
# # Source code
# You can find the code in the accompanying [`.py` file](https://github.com/arturomoncadatorres/lego-mindstorms/blob/main/examples/programs/hub_image_animation.py). To get it running, simply copy and paste it in a new Mindstorms project.
#
# # Imports

# %%
from mindstorms import MSHub, Motor, MotorPair, ColorSensor, DistanceSensor, App
from mindstorms.control import wait_for_seconds, wait_until, Timer
from mindstorms.operator import greater_than, greater_than_or_equal_to, less_than, less_than_or_equal_to, equal_to, not_equal_to
import math

# %%
import hub

# %%
print("-"*15 + " Execution started " + "-"*15 + "\n")

# %% [markdown]
# # Using `hub`
# Notice we won't be using the standard `MSHub`, but rather the "raw" `hub`.
# It is a little lower level, but it allows us making more things - like turning on the hub's pixels.
# Fore more information, see [Maarten Pennings brilliant explanation and unofficial documentation about it](https://github.com/maarten-pennings/Lego-Mindstorms/blob/main/ms4/faq.md#why-are-there-so-many-ways-to-do--in-python).

# %%
# Turn the central light off
hub.led(0, 0, 0)

# Alternatively, use
# hub.status_light.on('black')

# %% [markdown]
# # How to display an image
# Displaying an image is quite simple. We just need to define which pixels we will turn on and at what intensity.
# The pixel definition is done in a string in the shape
#
# `00000:00000:00000:00000:00000`
#
# where each number corresponds to a pixel. Each pixel can have a value between `0` (off) to `9` (on at full intensity).
# Each group of numbers (from left to right) correspond to a row of the hub (from top to bottom). 
# Notice the groups (i.e., rows) are separated by a colon `:`.
#
# Therefore, if we want to turn on the central pixel of the hub at full intensity, we can do the following:

# %%
print("Displaying example image...")
img_example = hub.Image('00000:00000:00900:00000:00000')
hub.display.show(img_example)
wait_for_seconds(5)
print("DONE!")

# %% [markdown]
# # How to display an animation
# After displaying an image, displaying an animation is quite straightforward, since an animation is
# basically displaying a succession of images. 
#
# In this example, we will display a very simple animation: a dot moving from top to bottom (with a tail). 
# However, the basic principle can be translated to more complicated animations. 
#
# I am sure there are plenty of ways to display an animation, but I found a simple way to do this is the following.
#
# First, we will define the frame of the animation in a list.

# %%

print("Defining animation frames...")

frames = ['00000:00000:00000:00000:00000',
'00900:00000:00000:00000:00000',
'00700:00900:00000:00000:00000',
'00500:00700:00900:00000:00000',
'00000:00500:00700:00900:00000',
'00000:00000:00500:00700:00900',
'00000:00000:00000:00500:00700',
'00000:00000:00000:00000:00500',
'00000:00000:00000:00000:00000']

n_frames = len(frames)

print("DONE!")


# %% [markdown]
# Then, we need to define the length of a pause between frames.
# The larger the pause, the slower the animation will be.

# %%
print("Defining delay between frames...")
t_pause = 0.05 # In seconds
print("DONE!")

# %% [markdown]
# Lastly, we display the frames (images) consecutively.
# This can be done very easily in a `for` loop.

# %%
print("Displaying animation...")

for ii in range(0, n_frames):
    img = hub.Image(frames[ii])
    hub.display.show(img)
    wait_for_seconds(t_pause)

print("DONE!")

# %% [markdown]
# That's it!

# %%
print("-"*15 + " Execution ended " + "-"*15 + "\n")
