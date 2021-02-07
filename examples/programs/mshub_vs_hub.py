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
# # `mshub_vs_hub`
# Comparison between the `mshub` and `hub` functionality.
#
# # Required robot
# * Hub
#
# <img src="../multimedia/hub.jpg" width="50%" align="center">
#
# # Source code
# You can find the code in the accompanying [`.py` file](https://github.com/arturomoncadatorres/lego-mindstorms/blob/main/examples/programs/mshub_vs_hub.py). To get it running, simply copy and paste it in a new Mindstorms project.
#
# # Imports

# %%
from mindstorms import MSHub, Motor, MotorPair, ColorSensor, DistanceSensor, App
from mindstorms.control import wait_for_seconds, wait_until, Timer
from mindstorms.operator import greater_than, greater_than_or_equal_to, less_than, less_than_or_equal_to, equal_to, not_equal_to
import math

#%%
import hub # Key to enable the `hub` functionality!

# %% [markdown]
# --------
# # Initialization
# #### Using `MSHub`
# We need to initialize it using
# 
# `hub = MSHub()`
#
# #### Using `hub`
# We don't need to initialize it. `hub` is already usable as it is.
#
# --------
# # Central button color
# ## Turning it on (with a color)
#
# ### Using `MSHub`
# Very straightforward, we just choose which color to display as follows
#
# `hub.status_light.on('blue')`
#
# See the [example `push_my_color`](https://github.com/arturomoncadatorres/lego-mindstorms/tree/main/examples) for a complete list of colors.
#
# ### Using `hub`
# In this case, we can choose a color using the command
#
# `hub.led(r, g, b)`
# 
# Where `r`, `g`, and `b` correspond to RGB values, respectively, with values between 0 and 255.
#
# So, if we want to turn it on blue

#%%
hub.led(0, 0, 255)
wait_for_seconds(5)

# %% [markdown]
# Alternatively, you can choose any predefined color by passing it a number, according to the following table:
#
# | Color | Number |
# |---------------|----------|
# | `pink`          | `1`   |
# | `violet`      | `2`   |
# | `blue`      | `3`   |
# | `azure`      | `4`   |
# | `cyan`      | `5`   |
# | `green`      | `6`   |
# | `yellow`      | `7`   |
# | `orange`      | `8`   |
# | `red`      | `9`   |
# | `white`      | `10`   |

#%%
hub.led(9)
wait_for_seconds(5)

# %% [markdown]
#
# ## Turning it off
#
# ### Using `MSHub`
# We display the `black` color
#
# `hub.status_light.on('black')`
#
# ### Using `hub`
# We just set all values to 0.

#%%
hub.led(0, 0, 0)
wait_for_seconds(5)

# %% [markdown]
# Alternatively, you can also use one 0
#
# `hub.led(0)`
#
# --------
# # Sounds
#
# ## Predefined beep sounds
# 
# ### Using `MSHub`
# Unfortunately, the library of predefined beep sounds is not available.
#
# ### Using `hub`
# We can play them very easily.

#%%
hub.sound.play("/extra_files/Target Destroyed")

# %% [markdown]
# The available sounds are given in the next table:
#
# | Original robot | Sound |
# |:---------------|-------|
# | **Blast**      | `Affirmative` |
# |                | `Damage` |
# |                | `Exterminate` |
# |                | `Fire` |
# |                | `Grab` |
# |                | `Hammer` |
# |                | `Laser` |
# |                | `Laugh` |
# |                | `Mission Accomplished` |
# |                | `Punch` |
# |                | `Scanning` |
# |                | `Seek and Destroy` |
# |                | `Shut Down` |
# |                | `Target Acquired` |
# |                | `Target Destroyed` |
# |                | `Whirl` |
# | **Charlie**    | `1234` |
# |                | `Delivery` |
# |                | `Dizzy` |
# |                | `Goodbye` |
# |                | `Hello` |
# |                | `Hi` |
# |                | `Hi 5` |
# |                | `Humming` |
# |                | `Chuckle` |
# |                | `Like` |
# |                | `No` |
# |                | `Ouch` |
# |                | `Sad` |
# |                | `Scared` |
# |                | `Tadaa` |
# |                | `Wow` |
# |                | `Yes` |
# |                | `Yipee` |
# |                | `Yuck` |
# | **Gelo**       | `Activate` |
# |                | `Kick` |
# |                | `Shake` |
# |                | `Deactivate` |
# |                | `Initialize` |
# | **MVP**        | `Brick Eating` |
# |                | `Horn` |
# |                | `Hydraulics Down` |
# |                | `Hydraulics Up` |
# |                | `Reverse` |
# |                | `Revving` |
# |                | `Shooting` |
# | **Tricky**     | `Bowling` |
# |                | `Celebrate` |
# |                | `Explosion` |
# |                | `Goal` |
# |                | `Hit` |
# |                | `Slam Dunk` |
# |                | `Strike` |
# | **Other**      | `Play` |
# |                | `Countdown` |
# |                | `Countdown Tick` |
# |                | `Error` |
# |                | `Ping` |
# |                | `Success Chime` |
#
# # References
# The content of this example is based on my experience, but also relies heavily in the following resources. Be sure to check them out for more!
#
# * [LEGO Mindstorms FAQ](https://github.com/maarten-pennings/Lego-Mindstorms/blob/main/ms4/faq.md) by Maarten Pennings
# * [Undocumented Python for LEGO Mindstorms](https://antonsmindstorms.com/2021/01/14/advanced-undocumented-python-in-spike-prime-and-mindstorms-hubs/) by Anton's Mindstorms <br>
