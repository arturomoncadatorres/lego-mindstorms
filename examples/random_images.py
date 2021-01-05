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
#  <img width="100%" src="../multimedia/mindstorms_51515_logo.png">
# </p>
#
# # `random_images`
# Display a set of random images in the hub
#
# # Required robot
# * Charlie (head)
#
# <img src="./multimedia/charlie_head.png" width="50%" align="center">
#
# # Source code
# You can find the code in the accompanying [`.py` file](https://github.com/arturomoncadatorres/lego-mindstorms/blob/main/examples/random_images.py). To get it running, simply copy and paste it in a new Mindstorms project.
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
hub = MSHub()

# %% [markdown]
# # Define the list of possible images

# %%
images = ['ANGRY', 'ARROW_E', 'ARROW_N', 'ARROW_NE', 'ARROW_NW',
'ARROW_S', 'ARROW_SE', 'ARROW_SW', 'ARROW_W', 'ASLEEP',
'BUTTERFLY', 'CHESSBOARD', 'CLOCK1', 'CLOCK10', 'CLOCK11', 
'CLOCK12', 'CLOCK2', 'CLOCK3', 'CLOCK4', 'CLOCK5', 
'CLOCK6', 'CLOCK7', 'CLOCK8', 'CLOCK9', 'CONFUSED', 
'COW', 'DIAMOND', 'DIAMOND_SMALL', 'DUCK', 'FABULOUS', 
'GHOST', 'GIRAFFE', 'GO_RIGHT', 'GO_LEFT', 'GO_UP', 
'GO_DOWN', 'HAPPY', 'HEART', 'HEART_SMALL', 'HOUSE',
'MEH', 'MUSIC_CROTCHET', 'MUSIC_QUAVER', 'MUSIC_QUAVERS', 'NO', 
'PACMAN', 'PITCHFORK', 'RABBIT', 'ROLLERSKATE', 'SAD', 
'SILLY', 'SKULL', 'SMILE', 'SNAKE', 'SQUARE', 
'SQUARE_SMALL', 'STICKFIGURE', 'SURPRISED', 'SWORD', 'TARGET', 
'TORTOISE', 'TRIANGLE', 'TRIANGLE_LEFT', 'TSHIRT', 'UMBRELLA', 
'XMAS', 'YES']

# %%
n_images = len(images)
print("Total number of images: " + str(n_images))

# %% [markdown]
# # Display images
# To choose the images to display, we will generate a random index
# using [`random.randint`](https://docs.python.org/3/library/random.html#random.randint)

# %%
for ii in range(1, 4):
    
    # Generate a random number
    idx = random.randint(0, n_images-1)

    # Display the random image
    image = images[idx]
    print("Displaying image " + str(ii) + " with index " + str(idx) + " ('" + image + "')...")
    hub.light_matrix.show_image(image)
    print("DONE!")

    # Insert a pause so we can see the image
    wait_for_seconds(2.5)
