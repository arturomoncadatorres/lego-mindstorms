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
# # `drum_master`
# Python equivalent of the `Drum master!` program. Charlie takes his drumming to a new level.
#
# This program is a direct follow-up of `drum_solo`. Actually, the first part is exactly the same.
# For the sake of shortness, I am not including the complete explanation of it (including
# the use of coroutines for "parallel" execution, which can be a bit overwhelming if you don't
# know what's going on). Therefore, if you want to know more about it, I invite you 
# to take a look at the [`drum_solo`](https://nbviewer.jupyter.org/github/arturomoncadatorres/lego-mindstorms/blob/main/base/charlie/programs/drum_solo.ipynb?flush_cache=True) program.
#
# # Required robot
# * Charlie (with advanced drum set)
#
# <img src="../multimedia/charlie_drummer_advanced.png" width="50%" align="center">
#
# However, during my testing, the drumsticks kept moving or falling, which was a bit frustrating. Thus, I adapted Charlie's hands grip to hold the drumsticks more steadily, as shown here. Basically, I replaced the fingertips with pins, where I snapped in the drumsticks:
#
# <table><tr>
# <td> <img src="../multimedia/charlie_drummer_fingertips_1.jpeg" alt="" style="width: 100%;"/> </td>
# <td> <img src="../multimedia/charlie_drummer_fingertips_2.jpeg" alt="" style="width: 100%;"/> </td>
# <td> <img src="../multimedia/charlie_drummer_fingertips_3.jpeg" alt="" style="width: 100%;"/> </td>
# <td> <img src="../multimedia/charlie_drummer_fingertips_4.jpeg" alt="" style="width: 100%;"/> </td>
# </tr></table>
#
# Much, much better.
#
# # Source code
# You can find the code in the accompanying [`.py` file](https://github.com/arturomoncadatorres/lego-mindstorms/blob/main/base/charlie/programs/drum_master.py). To get it running, simply copy and paste it in a new Mindstorms project.
#
# # Imports

# %%
from mindstorms import MSHub, Motor, MotorPair, ColorSensor, DistanceSensor, App
from mindstorms.control import wait_for_seconds, wait_until, Timer
from mindstorms.operator import greater_than, greater_than_or_equal_to, less_than, less_than_or_equal_to, equal_to, not_equal_to
import math

# %%
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
# # Overwrite `Timer`

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
# ## Define the `play_drums` function

# %%
timer_drums = Timer()
background_timer_left = Timer()
background_timer_right = Timer()

def play_drums(bars=4, tempo=100):

    """
    Makes Charlie play the drums.
    
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
    
    t_beat = 60 * (1/tempo)
    print("t_beat = " + str(t_beat))

    t_bar = t_beat * 4
    print("t_bar = " + str(t_bar))

    t_drumming = t_bar * bars
    print("t_drumming = " + str(t_drumming))


    def background_left_arm(t):
        """
        Parameters
        ----------
        t:
            Time (in seconds) for which the left arm will execute this action.
        """
        background_timer_left.reset() # Make sure timer is on 0.

        while background_timer_left.now() < t:
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

            t_action = yield

            if not t_action == None:

                motor_left_arm.start_at_power(50)
                yield from background_left_arm(t_action/2)
                motor_left_arm.start_at_power(-50)
                yield from background_left_arm(t_action/2)


    def drum_right_hand():

        while True:
            t_action = yield

            if not t_action == None:

                motor_right_arm.start_at_power(-25)    
                yield from background_right_arm((t_action/2)*4)
                motor_right_arm.start_at_power(25)
                yield from background_right_arm((t_action/2)*4)

    left_generator = drum_left_hand()
    right_generator = drum_right_hand()

    timer_drums.reset()
    while timer_drums.now() < t_drumming:
        
        next(left_generator)
        left_generator.send(t_beat)

        next(right_generator)
        right_generator.send(t_beat)

        wait_for_seconds(0.01)
        
        print(str(timer_drums.now()))

    return None


# %% [markdown]
# ## Repeat the part of `drum_solo`

# %%
print("Executing drum_solo part...")

# %%
app.start_sound('Triumph')
hub.light_matrix.show_image('MUSIC_QUAVER')

motor_left_arm.run_to_position(15)
motor_right_arm.run_to_position(345)

play_drums(bars=4, tempo=80)
play_drums(bars=4, tempo=130)

# %%
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

# %%
print("DONE!")

# %% [markdown]
# ## Actual `drum_master` part

# %%
motor_left_arm.run_to_position(60)
motor_right_arm.run_to_position(335)

# Hit that pedal, baby
print("Hitting the pedal...")
motors_wheels.move(3, unit='cm')
print("DONE!")

# %%
# Fire first drum blaster
print("Firing first drum blaster...")
motors_wheels.move(2.5, unit='cm', steering=-100)

for ii in range(0, 3):
    motor_right_arm.start_at_power(40)
    wait_for_seconds(0.12)
    motor_right_arm.start_at_power(-40)
    wait_for_seconds(0.12)
motor_right_arm.run_to_position(300, direction='shortest path')

motor_left_arm.run_for_seconds(0.5, speed=-100)
motor_left_arm.run_to_position(25, direction='shortest path')
print("DONE!")


# %%
# Fire second drum blaster
print("Firing second drum blaster...")
motors_wheels.move(5, unit='cm', steering=100)

for ii in range(0, 4):
    motor_left_arm.start_at_power(-40)
    wait_for_seconds(0.12)
    motor_left_arm.start_at_power(40)
    wait_for_seconds(0.12)
motor_left_arm.run_to_position(60, direction='shortest path')

motor_right_arm.run_for_seconds(0.5, speed=100)
motor_right_arm.run_to_position(345, direction='shortest path')
print("DONE!")

# %%
# Return to initial position
print("Returning to initial position...")
app.start_sound('Applause 3') # Charlie deserves some applause
motor_left_arm.run_to_position(15, direction='shortest path')
motors_wheels.move(2.5, unit='cm', steering=-100)
motors_wheels.move(-3, unit='cm')
print("DONE!")

# %%
print("-"*15 + " Execution ended " + "-"*15 + "\n")
