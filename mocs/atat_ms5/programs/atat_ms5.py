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
# # `atat_ms5`
# Python program to make the AT-AT MS5 robot walk.
# This time, the robot functionality is quite simple. The AT-AT MS5 just walks in a straight line.
#
# However, what is more interesting is how the motors are controlled. I used Anton's Mindstorms motor synchronization. This method is a very clever way to make two (or more) motors work together smoothly. This is particularly handy for the AT-AT MS5, since the legs movement have quite a peculiar pattern (more on that later).
#
# You can find a video of the robot functioning [here](TODO).
#
# # Required robot
# * AT-AT MS5 (you can find the [instructions for building it here](https://arturomoncadatorres.com/atat_ms5/))
#
# <img src="../multimedia/atat_ms5.jpg" width="50%" align="center">
#
# # Source code
# You can find the code in the accompanying [`.py` file](https://github.com/arturomoncadatorres/lego-mindstorms/blob/main/mocs/atat_ms5/programs/atat_ms5.py). To get it running, simply copy and paste it in a new MINDSTORMS project.
#
# # Imports
# Notice that we aren't using the default imports given by the MINDSTORMS app (e.g., `MSHub`), but rather the lower level [`hub`](https://antonsmindstorms.com/2021/01/14/advanced-undocumented-python-in-spike-prime-and-mindstorms-hubs/).

# %%
import hub
import utime
import math

# %%
print("-"*15 + " Execution started " + "-"*15 + "\n")


# %% [markdown]
# # Anton's MINDSTORMS motor synchronization
# We will be using [Anton's MINDSTORMS](https://antonsmindstorms.com/) technique for the motor synchronization. It is made of three main components:
#
# * A better timer
# * A motor animation mechanism
# * The definition of (the motors) metafunctions
#
# I will only cover the general concepts of each of them. If you want to learn more about their details, I suggest you take a look at Anton's [well-described tutorial](https://antonsmindstorms.com/2021/01/27/python-motor-synchronization-coordinating-multiple-spike-or-mindstorms-motors/) or, even better, [watch his explanation](https://www.youtube.com/watch?v=ctlRsDkKte8&ab_channel=AntonsMindstormsHacks) while coding in real-time. Moreover, Anton's code is nicely commented.
#
#
# ## Better timer
# First, we need to define a so-called better timer. That is because the original timer provided only has a resolutions of seconds. However, we need something much more precise. 
#
# The `AMHTimer` has a resolution of miliseconds. Moreover, it also allows us to stop it, reverse it, and even accelerate it. We won't be using such functionality for the AT-AT MS5, but maybe it will be useful for your robot! You probably don't want to mess with this at all.

# %%
class AMHTimer():
    """
    A configurable timer which you can start, reverse, stop and pause.
    By default, it counts milliseconds, but you can speed it up,
    Slow it down or accelerate it!
    You can also set the time and reset it.
    You can even run it in reverse, so you can count down until 0.
    It always returns integers, even when you slow it way down.

    Author: 
        Anton's Mindstorms Hacks - https://antonsmindstorms.com

    Usage:
        my_timer = AMHTimer():
        my_timer.rate = 500  # set the rate to 500 ticks/s. That is half the normal rate
        my_timer.acceleration = 100  # Increase the rate by 100 ticks/s^2
        my_timer.reset()  # Reset to zero. Doesn't change running/paused state
        now = mytimer.time  # Read the time
        mytimer.time = 5000  # Set the time
    """
    def __init__(self, rate=1000, acceleration=0):
        self.running = True
        self.pause_time = 0
        self.reset_at_next_start = False
        self.__speed_factor = rate/1000
        self.__accel_factor = acceleration/1000000
        self.start_time = utime.ticks_ms()

    @property
    def time(self):
        if self.running:
            elapsed = utime.ticks_diff( utime.ticks_ms(), self.start_time )
            return int(
                self.__accel_factor * elapsed**2 +
                self.__speed_factor * elapsed +
                self.pause_time
                )
        else:
            return self.pause_time

    @time.setter
    def time(self, setting):
        self.pause_time = setting
        self.start_time = utime.ticks_ms()

    def pause(self):
        if self.running:
            self.pause_time = self.time
            self.running = False

    def stop(self):
        self.pause()

    def start(self):
        if not self.running:
            self.start_time = utime.ticks_ms()
            self.running = True

    def resume(self):
        self.start()

    def reset(self):
        self.time = 0

    def reverse(self):
        self.rate *= -1

    @property
    def rate(self):
        elapsed = utime.ticks_diff(utime.ticks_ms(), self.start_time )
        return (self.__accel_factor*elapsed + self.__speed_factor) * 1000

    @rate.setter
    def rate(self, setting):
        if self.__speed_factor != setting/1000:
            if self.running:
                self.pause()
            self.__speed_factor = setting/1000
            self.start()

    @property
    def acceleration(self):
        return self.__accel_factor * 1000000

    @acceleration.setter
    def acceleration(self, setting):
        if self.__accel_factor != setting/1000000:
            if self.running:
                self.pause()
            self.__speed_factor = self.rate/1000
            self.__accel_factor = setting/1000000
            self.start()


# %% [markdown]
# ## Motor animation mechanism
# This is where the magic happens. Here, we define the central mechanism that actually animates the robot's motors. Similarly to the previous case, it is probably better if you leave this part untouched.

# %%
class Mechanism():
    """
    The class helps to control multiple motors in a tight loop.

    Author:
        Anton's Mindstorms Hacks - https://antonsmindstorms.com

    Args:
        motors: list of motor objects. Can be hub.port.X.motor or Motor('X')
        motor_functions: list of functions that take one argument and calculate motor positions

    Optional Args:
        reset_zero: bolean, resets the 0 point of the relative encoder to the absolute encoder position
        ramp_pwm: int, a number to limit maximum pwm per tick when starting. 0.5 is a good value for a slow ramp.
        Kp: float, proportional feedback factor for motor power.

    Returns:
        None.

    Usage:
        my_mechanism = Mechanism([Motor('A'), Motor('B')], [func_a, func_b])
        timer = AMHTimer()
        while True:
            my_mechanism.update_motor_pwms(timer.time)
    """
    def __init__(self, motors, motor_functions, reset_zero=True, ramp_pwm=100, Kp=1.2):
        # Allow for both hub.port.X.motor and Motor('X') objects:
        self.motors = [m._motor_wrapper.motor if '_motor_wrapper' in dir(m) else m for m in motors]
        self.motor_functions = motor_functions
        self.ramp_pwm = ramp_pwm
        self.Kp = Kp
        if reset_zero:
            self.relative_position_reset()

    def relative_position_reset(self):
        # Set degrees counted of all motors according to absolute 0
        for motor in self.motors:
            absolute_position = motor.get()[2]
            if absolute_position > 180:
                absolute_position -= 360
            motor.preset(absolute_position)

    @staticmethod
    def float_to_motorpower( f ):
        # Convert any floating point to number to
        # an integer between -100 and 100
        return min(max(int(f),-100),100)

    def update_motor_pwms(self, ticks):
        # Proportional controller toward desired motor positions at ticks
        for motor, motor_function in zip(self.motors, self.motor_functions):
            target_position = motor_function(ticks)
            current_position = motor.get()[1]
            power = self.float_to_motorpower((target_position-current_position)* self.Kp)
            
            if self.ramp_pwm < 100:
                # Limit pwm for a smooth start
                max_power = int(self.ramp_pwm*(abs(ticks)))
                if power < 0:
                    power = max(power, -max_power)
                else:
                    power = min(power, max_power)

            motor.pwm(power)

    def shortest_path_reset(self, ticks=0, speed=20):
        # Get motors in position smoothly before starting the control loop

        # Reset internal tacho to range -180,180
        self.relative_position_reset()

        # Run all motors to a ticks position with shortest path
        for motor, motor_function in zip(self.motors, self.motor_functions):
            target_position = int(motor_function(ticks))
            current_position = motor.get()[1]
            
            # Reset internal tacho so next move is shortest path
            if target_position - current_position > 180:
                motor.preset(current_position + 360)
            if target_position - current_position < -180:
                motor.preset(current_position - 360)
                
            # Start the maneuver
            motor.run_to_position(target_position, speed)
        
        # Give the motors time to spin up
        utime.sleep_ms(50)
        
        # Check all motors pwms until all maneuvers have ended
        while True:
            pwms = []
            for motor in self.motors:
                pwms += [motor.get()[3]]
            if not any(pwms): break
        
    def stop(self):
        for motor in self.motors:
            motor.pwm(0)


# %% [markdown]
# # Metafunction definition
# This is where I would like to spend some time, since this is key for customizing this approach to the AT-AT MS5. We need to define the movement of the motors as mathematical functions that describe them. Let's take this *piano piano*. 
#
# ## Identifying each leg
# First of all, let's make our life easier and give each leg an identifier. For the sake of simplicity, I will use a letter corresponding to the hub's port to where the leg's motor is connected.
#
# <img src="../multimedia/atat_legs.png" width="75%" align="center">
#
# ## Understanding the AT-AT movement
# Now, we need to understand the movement of an actual AT-AT. We could take a look at some [source material](https://www.youtube.com/watch?v=3acC49W3yQk), but that would probably would just make me want to rewatch the original trilogy. Instead, I found this very cool [computational model of an AT-AT walking](https://sketchfab.com/models/c5a4ab826eda4458aa748e252631735e/). It is fantastic. Try playing with it and move the camera around.
#
# It also has a [video equivalent](https://www.youtube.com/watch?v=GUsOouwjsL4), from which I extracted a GIF. Notice I purposefully left the crane at the beginning to make it easier to identify when the cycle begins.
#
# <img src="../multimedia/atat_walk.gif" width="75%" align="center">
#
# Paying close attention to the GIF, we can start describing the AT-AT's movement:
#
# 1. The order in which the legs move is `F`, `B`, `E`, and `A`.
# 1. At any moment, only one leg is in the air.
# 1. The movement speed of one leg when is in the air is faster than when it is in contact with the ground. 
#
# ## Translating the AT-AT movement into mathematical functions
# Anton's original code comes already with linear, sinusoidal, and block functions implemented. However, none of them accurately describe the AT-AT movement (and therefore I removed them from this script). Therefore, we need to dust our high school math and define them ourselves.
#
# I found that the most intuitive way is to do this graphically step by step. Let's start defining our plot for one leg only (let's say leg `F`). We will be looking at the motors' position $motor\_position$ (in degrees) as a function of time $t$ (in miliseconds). Moreover, we will define the period $T$ as the time it takes for a leg to do a complete cycle. Therefore:
#
# * When $t=0$, $motor\_position=0$
# * When $t=T$, $motor\_position=360$
#
# This would look something like this:
#
# <img src="../multimedia/plot1.png" width="75%" align="center">
#
# Now the trick is describing how to make it from the initial position to the final position. This is where our previous movement description becomes handy. We already defined that at any moment, only one leg of the AT-AT is in the air. Since we are talking about 4 legs, that means that each leg spends $T/4$ off the ground. Moreover, we can see from the GIF that during this time, the leg goes from 0 to 180$^{\circ}$. In consequence, it takes the leg the rest of the period ($3T/4$) to go from 180 to 360$^{\circ}$. Plotting this:
#
# <img src="../multimedia/plot2.png" width="75%" align="center">
#
# We are getting there! Now we just need to do the mathematical definition of the straight line ($y = mx + b$) for each segment.
#
# For the air segment:
#
# $$
# \begin{eqnarray}
# m_{air} &=& \frac{y_2-y_1}{x_2-x_1}\\
#         &=& \frac{180-0}{\frac{T}{4}-0}\\
#         &=& \frac{180\cdot4}{T}\\
#         &=& \frac{720}{T}\\ \\
# b_{air} &=& y - mx\\
#         &=& 180 - \frac{720}{T}\cdot\frac{T}{4}\\
#         &=& 180 - \frac{720}{4}\\
#         &=& 180 - 180\\
#         &=& 0
# \end{eqnarray}
# $$
#
# I guess we could have seen that from the plot, but I always like doing things a bit more systematically. Similarly, for the ground segment:
#
# $$
# \begin{eqnarray}
# m_{ground} &=& \frac{y_2-y_1}{x_2-x_1}\\
#         &=& \frac{360-180}{T-\frac{T}{4}}\\
#         &=& \frac{180}{\frac{3T}{4}}\\
#         &=& \frac{720}{3T}\\ 
#         &=& \frac{240}{T}\\ \\
# b_{ground} &=& y - mx\\
#         &=& 360 - \frac{240}{T}\cdot T\\
#         &=& 360 - 240\\
#         &=& 120
# \end{eqnarray}
# $$
#
# Therefore, the final function definition is given by:
#
# $$
# y = \left\{
# \begin{array}{ll}
#       \frac{720}{T} x &\mathrm{if}& 0 \leq x \leq \frac{T}{4} \\
#       \frac{240}{T} x + 120 &\mathrm{if}& \frac{T}{4} < x \leq T \\
# \end{array} 
# \right. 
# $$
#
# Now we just need to code that as a metafunction as follows. Pay attention to the comments, since they explain additional small (but important) considerations when doing the real implementation.

# %%
# Metafunction for AT-AT MS5 walking pattern
def atat_walk(factor=1, period=4000, t_shift=0):
    """
    Metafunction definition for making the AT-AT MS5 walk.
    
    Parameters
    ----------
    factor: integer
        Scaling factor. Larger numbers will increase the motor power.
        I recommend you use this one only to define the rotation direction of the motor (with +1 or -1).
        Default value is 1.
        
    period: integer
        Duration of a complete AT-AT walking cycle (in ms).
        Default value is 4000.
            
    t_shift: integer
        Shift in time (i.e., across the x axis) given in ms.
        Default value is 0.
        
    Returns
    -------
    function: function
    """
    def function(ticks):
        """
        ticks: integer
            Motor count.
            If used with the provided timer, it is given in ms.
        """
        
        # Adding a shift in the time axis allows us to delay (or hasten) 
        # the beggining of the motor movement.
        ticks = ticks + t_shift

        # Using the modulus operation, we make sure that our count is
        # always between 0 and T. For example:
        # if ticks = 6000 and period = 4000, ticks % period = 2000.
        # In other words, this operation allows the movement to be 
        # periodical (i.e., it keeps repeating itself every T).
        phase = ticks % period

        # Define the function depending on the given time.
        # This is nothing else but coding the mathematical function
        # that we derived earlier. However, you will see that we add 
        # an additional term: (ticks//period)*360
        # This term ensures that the counts of the motor keep incrementing
        # past 360 degrees. For example: if ticks = 6000 and period 4000, 
        # that means that the motor turned a full rotation already once. 
        # Mathematically:
        # (ticks//period)*360
        # = (6000//4000)*360
        # = 1 * 360
        # = 360
        # This way, the motor count can grow indefinitely. 
        # Without it, when the motor rotations pass 360 degrees, it will
        # go back to 0 abruptly (together with a terrible motor oscillation).
        if 0 <= phase <= (period//4):
            value = factor * ((720/period)*phase + (ticks//period)*360)
            return value
        else:
            value = factor * ((((240/period)*phase) + 120) + (ticks//period)*360)
            return value

    return function


# %% [markdown]
# # Defining movement parameters
# That was the most ellaborate part. From here on, it is quite simple, actually. We just need to define a few things. First, let's define the period $T$. In my experience, a value of 4000 (ms) works great (plus it made things very easy when debugging, since we are talking about 4 legs and 4 motors).

# %%
T = 4000

# %% [markdown]
# Then we need to define the motors. We will do so in the order they move (as discussed previously).

# %%
motor_f = hub.port.F.motor
motor_b = hub.port.B.motor
motor_e = hub.port.E.motor
motor_a = hub.port.A.motor

# %% [markdown]
# We also need to define their accompanying functions. In this case, notice how motors `F` and `B` have a factor of $-1$. That is to account their mirrored position in the body of the robot (compared to motors `E` and `A`). 
#
# Moreover, please also note how we give each motor a shift multiple of $T/4$. This way, we make sure that they move on the expected time. Notice that in the case of the motor `F`, `t_shift` could be either 0 or $T$ (since practically they correspond to the same point in time). 
#
# **Important!** Be aware that in order for these shift values to work correctly, you need to assemble the AT-AT MS5 exactly as defined in the instructions. If you connect the beams to different holes of the motor rotor, you will mess up the shift.

# %%
motor_f_function = atat_walk(-1, period=T, t_shift=0)
motor_b_function = atat_walk(-1, period=T, t_shift=3*T/4)
motor_e_function = atat_walk(1, period=T, t_shift=T/2)
motor_a_function = atat_walk(1, period=T, t_shift=T/4)

# %% [markdown]
# # Let the AT-AT MS5 walk!
# The last part is very straightforward. We just have to create a `Mechanism`, an `AMHTimer`, and make it run!

# %%
motors = [motor_a, motor_b, motor_e, motor_f]
motor_functions = [motor_a_function, motor_b_function, motor_e_function, motor_f_function]
atat_walk_mechanism = Mechanism(motors, motor_functions, ramp_pwm=50)

# Define timer
timer = AMHTimer()
timer.reset()

# Make the AT-AT MS5 walk!
print("Starting walk...")
while True:
    # For debugging purposes, you can print the value of the timer by
    # uncommenting the following line. Do note that this might
    # mess up the motor synchronization, since the timer is quite tight
    # and priting things takes time, even if it is only a fraction.
    # print("timer = " + str(timer.time))
    atat_walk_mechanism.update_motor_pwms(timer.time)

# Actually, we will actually never reach this point.
# However, I leave it here in case you decide to change
# the stopping condition of your robot.
atat_walk.stop()
print("DONE!")

print("-"*15 + " Execution ended " + "-"*15 + "\n")
