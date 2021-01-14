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
# # `push_my_color`
# Small game where the hub "thinks" of a random color and the player has to guess it
# by using the hub's buttons. The right button changes the color. The left button 
# confirms the player's guess.
#
# # Required robot
# * Charlie (head). This is only because it looks nice. However, the bare hub should work just fine.
#
# <img src="../multimedia/charlie_head.png" width="50%" align="center">
#
# # Source code
# You can find the code in the accompanying [`.py` file](https://github.com/arturomoncadatorres/lego-mindstorms/blob/main/examples/programs/push_my_color.py). To get it running, simply copy and paste it in a new Mindstorms project.
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
# If we set the button color to black, we turn it off.
hub.status_light.on('black')

# %% [markdown]
# # Choose random color
# Black is a bit of a boring color, so we will exclude it as a possibility.
# The other possible colors are:
# <table><tr>
# <td> <img src="../multimedia/azure.jpeg" alt="" style="width: 100%;"/> </td>
# <td> <img src="../multimedia/blue.jpeg" alt="" style="width: 100%;"/> </td>
# <td> <img src="../multimedia/cyan.jpeg" alt="" style="width: 100%;"/> </td>
# <td> <img src="../multimedia/green.jpeg" alt="" style="width: 100%;"/> </td>
# <td> <img src="../multimedia/orange.jpeg" alt="" style="width: 100%;"/> </td>
# <td> <img src="../multimedia/pink.jpeg" alt="" style="width: 100%;"/> </td>
# <td> <img src="../multimedia/red.jpeg" alt="" style="width: 100%;"/> </td>
# <td> <img src="../multimedia/violet.jpeg" alt="" style="width: 100%;"/> </td>
# <td> <img src="../multimedia/yellow.jpeg" alt="" style="width: 100%;"/> </td>
# <td> <img src="../multimedia/white.jpeg" alt="" style="width: 100%;"/> </td>
# </tr>
# <tr>
# <td> azure </td>
# <td> blue </td>
# <td> cyan </td>
# <td> green </td>
# <td> orange </td>
# <td> pink </td>
# <td> red </td>
# <td> violet </td>
# <td> yellow </td>
# <td> white </td>
# </tr>
# </table>

# %%
colors = ['azure', 'blue', 'cyan', 'green' ,'orange', 'pink', 'red', 'violet', 'yellow', 'white']
n_colors = len(colors)

# %%
print("Choosing a random color...")
idx = random.randint(0, n_colors-1)
chosen_color = colors[idx]

print("Chosen color is " + chosen_color + ". Shhh, don't tell anyone!")

# %% [markdown]
# # Start the game
# We will keep track of which color to display using a counter.
# The counter will increment with each press of the right button.
# The actual index of the color list will be calculated using the
# mod operator (`%`). This allows us to always stay within a range
# of numbers, even if the counter keeps increasing.

# %%
counter = 0
guessed_color = colors[0]

# %%
# We will loop as long as the user doesn't guess correctly.
correct_guess = False
while correct_guess == False:

    # Convert the counter to an index of the colors list.
    color_idx = counter % n_colors

    # Turn on the button with the corresponding color.
    hub.status_light.on(colors[color_idx])

    if hub.right_button.was_pressed():
        # If the right button was pressed, increase the counter by one
        # and shift the color_idx.
        counter += 1
        color_idx = counter % n_colors
        print("Right button changed color to " + colors[color_idx] + "(color_idx = " + str(color_idx) + "; counter = " + str(counter) + ")")

    if hub.left_button.was_pressed():
        # If the left button was pressed, save the current color as the player's guess.
        guessed_color = colors[color_idx]
        print("Guessed color is " + guessed_color)

        # Check if the player's guess was correct.
        if guessed_color == chosen_color:

            # If the user guessed the color, provide positive feedback.
            # (S)he won!
            app.start_sound('Tada')
            hub.light_matrix.show_image('YES')
            correct_guess = True # This makes sure we won't go through the loop again.

            print("That is correct :) ! The chosen color was " + guessed_color + ". You win!")
            

        else:
            # If the user didn't guess the color, provide negative feedback.
            app.start_sound('Lose')
            hub.light_matrix.show_image('NO')
            wait_for_seconds(4)
            hub.light_matrix.off()

            # To make things easier for the player, we will remove the wrong
            # color of the list, so it isn't displayed again.
            colors.pop(color_idx)
            n_colors = len(colors)

            if color_idx == n_colors:
                # If the guessed color was the last one, we will reset the counter,
                # to make sure that the next color to be displayed is the first one.
                counter = 0

            else:
                # If the guessed color wasn't the last one, we set the counter
                # to the color index, to account for the removed color.
                counter = color_idx

            # Just for clarity.
            correct_guess = False

            print("That is incorrect :( . Color " + guessed_color + " was removed.")


# %%
print("-"*15 + " Execution ended " + "-"*15 + "\n")
