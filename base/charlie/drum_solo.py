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
# # `drum_solo`
# Python equivalent of the `Drum solo` program. Enjoy Charlie's performance.
#
# This program was particularly challenging, since replicating the block `Charlie plays drums`
# required async execution. Usually, you can do so in Python using threads. 
# However, they have a [couple of drawbacks](https://effectivepython.com/2015/03/10/consider-coroutines-to-run-many-functions-concurrently):
#
# * They can be hard to coordinate
# * They require a lot of memory (~8 MB each)
# * They have huge overhead (in other words, they can be slow)
# * Most importantly for us: MicroPython doesn't support it.
#
# Thus, we need to look for other workarounds. Namely, we will be using coroutines. 
# The solution in this script is built using [this code piece written by David Lechner](https://gist.github.com/dlech/fa48f9b2a3a661c79c2c5880684b63ae).
# Full credit goes to him. The use of coroutines in this program is explained later on (inside the function `play_drums`).
#
# # Required robot
# * Charlie (with basic drum set)
#
# <img src="./multimedia/charlie_drummer.png" width="50%" align="center">
#
# # Source code
# You can find the code in the accompanying [`.py` file](https://github.com/arturomoncadatorres/lego-mindstorms/blob/main/base/charlie/charlie_drummer.py). To get it running, simply copy and paste it in a new Mindstorms project.
#
# # Imports

# %%
from mindstorms import MSHub, Motor, MotorPair, ColorSensor, DistanceSensor, App
from mindstorms.control import wait_for_seconds, wait_until, Timer
from mindstorms.operator import greater_than, greater_than_or_equal_to, less_than, less_than_or_equal_to, equal_to, not_equal_to
import math

# %%
# Required for our own timer implementation.
from utime import sleep as wait_for_seconds
from utime import ticks_diff, ticks_ms

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
print("DONE!")

# %% [markdown]
# # Set arm motors to starting position

# %%
print("Setting arm motors to position 0...")
motor_left_arm.run_to_position(0)
motor_right_arm.run_to_position(0)
print("DONE!")

# %% [markdown]
# # Overwrite `Timer`
# Unfortunately, `mindstorms.control.Timer` doesn't support floats.
# Thus, we need to define our own timer (using the functionality of `utime`).

# %%
print("Overwriting timer...")

class Timer():
    """
    Replacement Timer class that allows using floats (i.e., seconds with a decimal place). 
    """

    def __init__(self):
        """
        Initialization
        """
        self.start_ticks = 0

    def now(self):
        """
        Returns the time (in seconds) since the timer was last reset.
        """
        return ticks_diff(ticks_ms(), self.start_ticks) / 1000

    def reset(self):
        """
        Resets the timer
        """
        self.start_ticks = ticks_ms()

print("DONE!")

# %% [markdown]
# # Make Charlie drum away
#
# First, we need to define a function for playing the drums
# (equivalent to the block `Charlie plays drums`).
#
# Notice how we can define the default values of a function
# (in this case, `bars=4` and `tempo=100`). Moreover, 
# it is great practice that every time that we define a function,
# we describe how it works (namely, what parameters it expects 
# and what it returns).

# %%
timer_drums = Timer()
background_timer_left = Timer()
background_timer_right = Timer()

def play_drums(bars=4, tempo=100):

    """
    Makes Charlie play the drums.
    I had to read a bit into music to get the concept of bars and tempo.
    More importantly, it uses coroutines to simulate async execution
    of the arm motors. Both of them are a first time for me.
    My apologies if my explantion of any of them isn't completely accurate.
    
    Parameters
    ----------
    bars:
        Number of bars (in our case, simple number of cycles).
        Default value is 4.
    tempo:
        Playing tempo (in bpm).
        Default value is 100
            
    Returns
    -------
    None
    """
    
    # First, we will calculate how much should each beat last.
    # We will convert the tempo [beats per minute] to period [s].
    t_beat = 60 * (1/tempo)
    print("t_beat = " + str(t_beat))

    # Now, we will calculate how much each bar should last.
    # We will assume a 4/4 tune.
    t_bar = t_beat * 4
    print("t_bar = " + str(t_bar))

    # Lastly, we will calculate how much the whole drumming should last.
    t_drumming = t_bar * bars
    print("t_drumming = " + str(t_drumming))

    # Now, this is where things get interesting. Bear with me.
    # First, we need to define the coroutines.
    # We need to define two: one for each arm (pretty much identical).
    # Notice how the definition is very similar to that of a function.
    # Coroutines also have input parameters.
    # However, there is no "output" (i.e., return), but actually a yield.
    def background_left_arm(t):
        """
        Parameters
        ----------
        t:
            Time (in seconds) for which the left arm will execute this action.
        """
        background_timer_left.reset() # Make sure timer is on 0.

        # Here, we check if the execution time of this arm has exceeded
        # the desired duration (given by t).
        while background_timer_left.now() < t:
            
            # If it hasn't, we reach this yield.
            # yield lets the rest of the program run until we come back
            # here again later to check if the condition was met.
            yield

    def background_right_arm(t):
        """
        Parameters
        ----------
        t:
            Time (in seconds) for which the right arm will execute this action.
        """
        background_timer_right.reset()
        while background_timer_right.now() < t:
            yield

    def drum_left_hand():
        while True:

            # This is how we receive a parameter.
            # In this case, it corresponds to the time the action should last.
            t_action = yield

            # We make sure we only execute code if the received
            # value was transmitted correctly.
            if not t_action == None:
                # We will start to move the arm downwards...
                motor_left_arm.start_at_power(50)
                
                # ...and check if its duration exceeded the maximum allowed.
                # Notice that we need to divide t_action by 2, since the action
                # is composed of moving the arm downwards (first half)...
                yield from background_left_arm(t_action/2)

                # ...and upwards (second half, same process).
                motor_left_arm.start_at_power(-50)
                yield from background_left_arm(t_action/2)

                # We assume that the movement is immediate and takes no time.
                # This isn't completely true, but for now it works.


    def drum_right_hand():

        while True:
            t_action = yield

            if not t_action == None:
                # It is worth mentioning a few things regarding the right arm's movement.
                # - First, that we multiply t_action by 4 (since we are in a 4/4 tune).
                # This is because we want the right arm to take the time of 4 beats.
                # - Then, notice that the right arm also uses a lower power. Otherwise
                # its trajectory is much longer. Originally, I wanted to try with 12.5 (rounded to 13)
                # (a reduction by a factor of 4). Unfortunately, that wasn't enough to move
                # the arm at all. Thus, I settled for a factor of 2.
                motor_right_arm.start_at_power(-25)    
                yield from background_right_arm((t_action/2)*4)
                motor_right_arm.start_at_power(25)
                yield from background_right_arm((t_action/2)*4)

    # Since the drum_left_hand() and drum_right_hand() are coroutines and use yield
    # (i.e., they are not functions and thus have no return), they will NOT
    # run here when we call them. Instead, they will just be created as generator objects.
    # These generators will be used to run the functions one yield (i.e., step) at a time.
    left_generator = drum_left_hand()
    right_generator = drum_right_hand()

    # Now we will actually start the task.
    # The task (playing the drums) will be run as long as its
    # execution time is shorter than the allowed max duration (t_drumming).
    timer_drums.reset()
    while timer_drums.now() < t_drumming:
        
        next(left_generator)
        left_generator.send(t_beat) # We send t_beat to the generator.

        next(right_generator)
        right_generator.send(t_beat)

        wait_for_seconds(0.01) # Small pause between steps.
        
        # We also print the time in console.
        print(str(timer_drums.now()))

    return None


# %% [markdown]
# Now we can actually drum away!

# %%
print("Starting drumming...")

app.start_sound('Triumph')
hub.light_matrix.show_image('MUSIC_QUAVER')

motor_left_arm.run_to_position(15)
motor_right_arm.run_to_position(345)

play_drums(bars=4, tempo=80)
play_drums(bars=4, tempo=130)

print("DONE!")


# %%
print("Going for the finale...")

motor_left_arm.run_to_position(15)
motor_right_arm.run_to_position(345)

for ii in range(0, 8):

    wait_for_seconds(0.1)
    motors_arms.start_at_power(50, steering=-100)
    wait_for_seconds(0.1)
    motors_arms.start_at_power(-50, steering=-100)

app.play_sound('Tada')
motor_left_arm.run_to_position(0, direction='shortest path')
motor_right_arm.run_to_position(0, direction='shortest path')

print("DONE!")


# %%
print("-"*15 + " Execution ended " + "-"*15 + "\n")
