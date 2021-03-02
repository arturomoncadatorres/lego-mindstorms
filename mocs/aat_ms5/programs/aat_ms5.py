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
# # `aat_ms5`
# Python program to control the AAT MS5 robot on patrol mode.
# The tank will move in circles, while the droid in the blaster will be looking for any sympathisants of the Republic.
# When the distance sensor detects a target, the tank will stop and the droid will center the
# blasters to fire! 
#
# You can find a video of the robot functioning [here](https://www.youtube.com/watch?v=Ma7CmThktUg&feature=youtu.be&ab_channel=ArturoMoncada-Torres).
#
# # Required robot
# * AAT MS5 (you can find the [instructions for building it here](https://arturomoncadatorres.com/aat-ms5/))
#
# <img src="../multimedia/aat_ms5.png" width="50%" align="center">
#
# # Source code
# You can find the code in the accompanying [`.py` file](https://github.com/arturomoncadatorres/lego-mindstorms/blob/main/mocs/aat_ms5/programs/aat_ms5.py). To get it running, simply copy and paste it in a new Mindstorms project.
#
# # Imports

# %%
from mindstorms import MSHub, Motor, MotorPair, ColorSensor, DistanceSensor, App
from mindstorms.control import wait_for_seconds, wait_until, Timer
from mindstorms.operator import greater_than, greater_than_or_equal_to, less_than, less_than_or_equal_to, equal_to, not_equal_to
import math

import hub

# %%
print("-"*15 + " Execution started " + "-"*15 + "\n")

# %% [markdown]
# # Initialize hub
# Notice we won't be using the standard `MSHub`, but rather the "raw" `hub`.
# It is a little lower level, but it allows us making more things. 
# Fore more information, see [Maarten Pennings brilliant explanation and unofficial documentation about it](https://github.com/maarten-pennings/Lego-Mindstorms/blob/main/ms4/faq.md#why-are-there-so-many-ways-to-do--in-python).

# %%
# hub = MSHub()

# %%
# hub.status_light.on('black')
hub.led(0, 0, 0)

# %% [markdown]
# # Initialize motors

# %%
print("Configuring motors...")
motor_steer = Motor('A') # Front wheels (for steering)
motor_power = Motor('C') # Back wheels (for moving)

motor_turret = Motor('B') # Turrent spinning

# %%
print("Setting motors to position 0...")
motor_steer.run_to_position(45, speed=100)
motor_steer.run_to_position(0, speed=100)

motor_turret.run_to_position(0, speed=75)
print("DONE!")


# %% [markdown]
# # Initialize distance sensor

# %%
print("Initializing distance sensor...")
distance_sensor = DistanceSensor('D')
print("DONE!")


# %% [markdown]
# # Put the AAT MS5 in motion
#
# The tank will move until the distance sensor detects an obstacle.
#
# The steering is given by `POSITION`. 
# * A value between `0` and `90` will steer the tank to the left.
#     - A value closer to `0` will make the tank turn wider.
#     - A value closer to `90` will make the tank turn tighter.
#
# * A value between `270` and `360` will steer the tank to the right.
#     - A value closer to `270` will make the tank turn tighter.
#     - A value closer to `360` will make the tank turn wider.
# %%
POSITION = 270

print("Steering...")
motor_steer.run_to_position(POSITION, speed=35)
print("DONE!")

# %% [markdown]
# The tank speed is given by `SPEED`. It should have a value between `-100` and `100`.
# * A negative value will move the tank forward.
# * A positive value will move the tank backwards.
#
# Recommended value is `-50`
# %%
SPEED = -50

print("Moving...")
motor_power.start(SPEED)
print("DONE!")

# %% [markdown]
# # Configure the patrolling
# We will move the turret constantly. It will go from left to right and from 
# right to left. When an obstacle is detected, the turret will go back to the
# initial position and "fire".
#
#
#
# ## Define distance function
# As part of the program, we need to continuously check if the
# measured distance is less than 10 cm. 

# %%
OBSTACLE_DISTANCE = 10 # [cm]


# %% [markdown]
# However, if the sensor reads no measure, it will return a `None`, which
# in turn will generate an error (since we cannot do a comparision
# between a `None` and something else).
#
# To solve this, we will define our own cuestom distance function.
# This way, when the sensor has no reading, we will just return
# a (simulated) very long distance (instead of returning a `None`).
# This will allow us to safely do the comparision.

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
        distance = 10000
        
    return distance


# %% [markdown]
# ## Patrolling
# Now, in order to be able to stop the turret at any moment 
# (and not until the motor has completed a whole sweep), 
# we will use co-routines. 
#
# > This is a simplified version [David Lechner's trick](https://community.legoeducation.com/discuss/viewtopic/66/110), which I've used before in [Charlie's `drum_solo`](https://nbviewer.jupyter.org/github/arturomoncadatorres/lego-mindstorms/blob/main/base/charlie/programs/drum_solo.ipynb?flush_cache=True).
# In this case, we are only controlling one motor (the turret) and we don't depend on time
# (but rather on the motor position). Thus, we don't need a timer.
#
# We need to define a function for moving the turret. 
# Pay attention to the comments, since they explain how using
# co-routines work. It isn't very hard, but it isn't trivial either.

# %%
def move_turret():

    """
    Moves the AAT MS5 turrent.
    
    Parameters
    ----------
    None
            
    Returns
    -------
    None
    """
    
    # First, we need to define the coroutine.
    # In this case, we only need one (corresponding to the turret motor).
    # Notice how the definition is very similar to that of a function.
    # Coroutines also have input parameters.
    # However, they have no "output" (i.e., return), but actually a yield.
    def background_turret(angle):
        """
        Parameters
        ----------
        angle:
            The angle at which the turret turns. 
            In practice, this value is twice the original angle, since
            it moves completely from one side to the other (and not from
            the center to one side). That is why it is passed to this 
            function multiplied by two.
            
            In degrees.
        """
        
        # We want to make sure counted degrees are initialized at 0.
        motor_turret.set_degrees_counted(0)
        
        # Notice that we use the absolute value of the counted degrees.
        # This is to ensure that it works on the way back (when the measured
        # degrees would be negative).
        curr_turret_position = math.fabs(motor_turret.get_degrees_counted())

        # Here, we check if the motor has reached the desired angle.
        while curr_turret_position < angle:
            
            # If you wish to see the current turret position and the target angle,
            # uncomment the following line.
            # print(str(curr_turret_position) + " - " +  str(angle))
            
            # We update the turret current position.
            curr_turret_position = math.fabs(motor_turret.get_degrees_counted())
            
            # If the turret hasn't reached the desired angle, we reach this yield.
            # yield lets the rest of the program run until we come back
            # here again later to check if the condition was met.
            yield


    def turret_patrol():
        while True:

            # This is how we receive a parameter.
            # In this case, it corresponds to the angle the motor should move.
            angle_action = yield

            # We make sure we only execute code if the received
            # value was transmitted correctly.
            if not angle_action == None:
                
                # We will start to move the turret...
                motor_turret.start(10)
                
                # ...and check if its angle exceeded the maximum allowed.
                # First we move the turret from left to right...
                yield from background_turret(angle_action*2)
                hub.sound.beep(150, 200, hub.sound.SOUND_SIN) # Play simple tone


                # ...and from right to left (exactly same process, but inverted speed).
                motor_turret.start(-10)
                yield from background_turret(angle_action*2)
                # hub.sound.play("/extra_files/Ping")
                hub.sound.beep(150, 200, hub.sound.SOUND_SIN) # Play simple tone

                # We assume that the movement is immediate and takes no time.
                # This isn't completely true, but for now it works.

    # Since turret_patrol() is a coroutine and uses yield
    # (i.e., it isn't a function and thus has no return), it will NOT
    # run here when we call it. Instead, it will just be created as a generator object.
    # This generator will be used to run the functions one yield (i.e., step) at a time.
    turret_generator = turret_patrol()

    # Now we will actually start the task.
    # The task (turret patrolling) will be run as long as the distance sensor
    # doesn't detect an obstacle.
    while my_get_distance_cm() > OBSTACLE_DISTANCE:
        
        next(turret_generator)
        turret_generator.send(TURRET_ANGLE)

        wait_for_seconds(0.01) # Small pause between steps.

    return None


# %% [markdown]
# After we have defined the turret movement, we can now make the AAT MS5 patrol until it finds those pesky Republic supporters!

# %%
TURRET_ANGLE = 40

print("Initializing turret with angle " + str(TURRET_ANGLE) + "...")
motor_turret.set_default_speed(10)
motor_turret.run_for_degrees(-TURRET_ANGLE)
print("DONE!")

print("Starting patrolling...")
move_turret()
print("DONE!")

# %% [markdown]
# Once it finds an enemy (i.e, it detects an obstacle), it will stop and center the turret.

# %%
print("Enemy detected! Attack!")
motor_power.stop() # Stop the movement
motor_turret.run_to_position(0, speed=75) # Center the turret

# %% [markdown]
# Then, it will fire three blasters. Each blaster will come with a sound and an
# animation of the blaster moving in the hub.
#
# First, lets define the frames of the animation.

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
t_pause = 0.05 # Pause between frames (in seconds)

print("DONE!")


# %% [markdown]
# Then, let's proceed with the actual fire!

# %%
print("Firing blasters...")

n_blasters = 3

for ii in range(0, n_blasters):

    # Play blaster sound.
    hub.sound.play("/extra_files/Laser")

    # Display blaster animation.
    for ii in range(0, n_frames):
        img = hub.Image(frames[ii])
        hub.display.show(img)
        wait_for_seconds(t_pause)

    wait_for_seconds(0.5)

print("DONE!")

# %%
print("Target eliminated.")

# %%
print("-"*15 + " Execution ended " + "-"*15 + "\n")
