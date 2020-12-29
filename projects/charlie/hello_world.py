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

# %% [markdown]
# # Initialization.

# %%
hub = MSHub()
app = App()

# %% [markdown]
# # Set color of center button
# Possible values of color are:
# 
# * `azure` (probably my favorite)
# * `black` (turns it off)
# * `blue`
# * `cyan`
# * `green`
# * `orange`
# * `pink`
# * `red`
# * `violet`
# * `yellow`
# * `white` (default)

# %%
button_color = 'black'
print("Turning color of center button to " + button_color + "...")
hub.status_light.on(button_color)
print("DONE!")

# %% [markdown]
# # Set orientation
# At the time of writing, there is no equivalent in Micropython
# to the "set orientation to" block. This means that we are stuck
# with a default orientation of upright.

# %% [markdown]
# # Start animation.
# At the time of writing, there is no equivalent in Python
# to the "start animation" block. However, we can display images in the hub.
# Possible animations are (notice that they need to be in caps):
#    
# * `ANGRY`
# * `ARROW_E`
# * `ARROW_N`
# * `ARROW_NE`
# * `ARROW_NW`
# * `ARROW_S`
# * `ARROW_SE`
# * `ARROW_SW`
# * `ARROW_W`
# * `ASLEEP`
# * `BUTTERFLY`
# * `CHESSBOARD`
# * `CLOCK1`
# * `CLOCK10`
# * `CLOCK11`
# * `CLOCK12`
# * `CLOCK2`
# * `CLOCK3`
# * `CLOCK4`
# * `CLOCK5`
# * `CLOCK6`
# * `CLOCK7`
# * `CLOCK8`
# * `CLOCK9`
# * `CONFUSED`
# * `COW`
# * `DIAMOND`
# * `DIAMOND_SMALL`
# * `DUCK`
# * `FABULOUS`
# * `GHOST`
# * `GIRAFFE`
# * `GO_RIGHT`
# * `GO_LEFT`
# * `GO_UP`
# * `GO_DOWN`
# * `HAPPY`
# * `HEART`
# * `HEART_SMALL`
# * `HOUSE`
# * `MEH`
# * `MUSIC_CROTCHET`
# * `MUSIC_QUAVER`
# * `MUSIC_QUAVERS`
# * `NO`
# * `PACMAN`
# * `PITCHFORK`
# * `RABBIT`
# * `ROLLERSKATE`
# * `SAD`
# * `SILLY`
# * `SKULL`
# * `SMILE`
# * `SNAKE`
# * `SQUARE`
# * `SQUARE_SMALL`
# * `STICKFIGURE`
# * `SURPRISED`
# * `SWORD`
# * `TARGET`
# * `TORTOISE`
# * `TRIANGLE`
# * `TRIANGLE_LEFT`
# * `TSHIRT`
# * `UMBRELLA`
# * `XMAS`
# * `YES`

# %%
image = 'HEART'
brightness = 75

# %%
print("Starting animation '" + image  + "' with brightness " + str(brightness) + "...")
hub.light_matrix.show_image(image, brightness)
print("DONE!")

# %% [markdown]
# Unfortuantely, Micropython doesn't support f-strings.
# Thus, notice how if we want to print a number, we need to cast it as a string.
#
# # Play sound
# At the time of writing, there is no equivalent in Micropython
# to playing sounds from the hub. This means that we are stuck
# with playing sounds only from the system (e.g., computer, tablet)
# where we are programming. Possible sounds are:
#
# * `Alert`
# * `Applause 1` or `Applause 2` or `Applause 3`
# * `Baa`
# * `Bang 1` or `Bang 2`
# * `Basketball Bounce`
# * `Big Boing`
# * `Bird`
# * `Bite`
# * `Boat Horn 1` or `Boat Horn 2`
# * `Bonk`
# * `Boom Cloud`
# * `Boop Bing Bop`
# * `Bowling Strike`
# * `Burp 1` or `Burp 2` or `Burp 3`
# * `Car Accelerate 1` or `Car Accelerating 2`
# * `Car Horn`
# * `Car Idle`
# * `Car Reverse`
# * `Car Skid 1` or `Car Skid 2`
# * `Car Vroom`
# * `Cat Angry`
# * `Cat Happy`
# * `Cat Hiss`
# * `Cat Meow 1` or `Cat Meow 2` or `Cat Meow 3`
# * `Cat Purring`
# * `Cat Whining`
# * `Chatter`
# * `Chirp`
# * `Clang`
# * `Clock Ticking`
# * `Clown Honk 1` or `Clown Honk 2` or `Clown Honk 3`
# * `Coin`
# * `Collect`
# * `Connect`
# * `Crank`
# * `Crazy Laugh`
# * `Croak`
# * `Crowd Gasp`
# * `Crunch`
# * `Cuckoo`
# * `Cymbal Crash`
# * `Disconnect`
# * `Dog Bark 1` or `Dog Bark 2` or `Dog Bark 3`
# * `Dog Whining 1` or `Dog Whining 2`
# * `Doorbell 1` or `Doorbell 2` or `Doorbell 3`
# * `Door Closing`
# * `Door Creek 1` or `Door Creek 2`
# * `Door Handle`
# * `Door Knock`
# * `Door Slam 1` or `Door Slam 2`
# * `Drum Roll`
# * `Dun Dun Dunnn`
# * `Emotional Piano`
# * `Fart 1` or `Fart 2` or `Fart 3`
# * `Footsteps`
# * `Gallop`
# * `Glass Breaking`
# * `Glug`
# * `Goal Cheer`
# * `Gong`
# * `Growl`
# * `Grunt`
# * `Hammer Hit`
# * `Head Shake`
# * `High Whoosh`
# * `Jump`
# * `Jungle Frogs`
# * `Laser 1` or `Laser 2` or `Laser 3`
# * `Laughing Baby 1` or `Laughing Baby 2`
# * `Laughing Boy`
# * `Laughing Crowd 1` or `Laughing Crowd 2`
# * `Laughing Girl`
# * `Laughing Male`
# * `Lose`
# * `Low Boing`
# * `Low Squeak`
# * `Low Whoosh`
# * `Magic Spell`
# * `Male Jump 1` or `Male Jump 2`
# * `Moo`
# * `Ocean Wave`
# * `Oops`
# * `Orchestra Tuning`
# * `Party Blower`
# * `Pew`
# * `Ping Pong Hit`
# * `Plane Flying By`
# * `Plane Motor Running`
# * `Plane Starting`
# * `Pluck`
# * `Police Siren 1` or `Police Siren 2` or `Police Siren 3`
# * `Punch`
# * `Rain`
# * `Ricochet`
# * `Rimshot`
# * `Ring Tone`
# * `Rip`
# * `Robot 1` or `Robot 2` or `Robot 3`
# * `Rocket Explosion Rumble`
# * `Rooster`
# * `Scrambling Feet`
# * `Screech`
# * `Seagulls`
# * `Service Announcement`
# * `Sewing Machine`
# * `Ship Bell`
# * `Siren Whistle`
# * `Skid`
# * `Slide Whistle 1` or `Slide Whistle 2`
# * `Sneaker Squeak`
# * `Snoring`
# * `Snort`
# * `Space Ambience`
# * `Space Flyby`
# * `Space Noise`
# * `Splash`
# * `Sport Whistle 1` or `Sport Whistle 2`
# * `Squeaky Toy`
# * `Squish Pop`
# * `Suction Cup`
# * `Tada`
# * `Telephone Ring` or `Telephone Ring 2`
# * `Teleport` or `Teleport 2` or `Teleport 2`
# * `Tennis Hit`
# * `Thunder Storm`
# * `Toliet Flush`
# * `Toy Honk`
# * `Toy Zing`
# * `Traffic`
# * `Train Breaks`
# * `Train Horn 1` or `Train Horn 2` or `Train Horn 3`
# * `Train On Tracks`
# * `Train Signal 1` or `Train Signal 2`
# * `Train Start`
# * `Train Whistle`
# * `Triumph`
# * `Tropical Birds`
# * `Wand`
# * `Water Drop`
# * `Toliet Flush` (TODO: check spelling)
# * `Whiz 1` or `Whiz 2`
# * `Window Breaks`
# * `Win`
# * `Wobble`
# * `Wood Tap`
# * `Zip`

# %%
sound = 'Tada'
volume = 75

# %%
print("Playing sound '" + sound + "' with volume " + str(volume) + "...")
app.play_sound(sound, volume)
print("DONE!")
