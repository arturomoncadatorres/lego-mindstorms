<img src="./multimedia/mindstorms_51515.png" width="100%" align="center">

This repository hosts my LEGO Mindstorms projects. All of them use the electronics of the [51515 set](https://www.lego.com/en-us/product/robot-inventor-51515) and are programmed using (Micro)Python. I've grouped them in three categories:

* **Base projects**<br>
The [LEGO Mindstorms 51515 software](https://www.microsoft.com/en-us/p/lego-mindstorms-robot-inventor/9mtq0n7w1d6x) already comes with several programs for the different robots. However, these are programmed using Scratch. In this directory you will find their counterparts in Python.

<img src="./multimedia/mindstorms_robots.png" width="75%" align="center">

* **[Example scripts](https://github.com/arturomoncadatorres/lego-mindstorms/tree/main/examples)**<br>
A few example scripts that I've created to test or experiment some functionality that I thought would be worth sharing.

* **Original projects**<br>
Here I've documented my own creations. For each of them, I've included the building instructions for the robot (as a PDF), as well as its corresponding (Python) program, so that anyone can reproduce them and, most importantly, improve them.


## My setup
Although technically the 51515 hub can be programmed in Python, its support is quite limited. You are restricted to writing code in Python within the LEGO Mindstorms app (either in your laptop, tablet, or mobile), locking you out of using your preferred (and probably more powerful) IDE. Moreover, each project is saved as an `.lms` file, regardless if it is written in Scratch or Python. `.lms` files are binary and thus cannot be put under version control.

Given these restrictions, this is how I've configured my setup for the development and documentation of my LEGO Mindstorms projects using Python:

* First, I start coding on the LEGO Mindstorms app. I take advantage of pre-defined imports (which otherwise I would forget), and of the so-called "Knowledge Base" (which is nothing else than the documentation). When the hub is linked, I like how you can see in real-time the status of the motors and sensors connected to it. I always keep the console open (at the bottom of the screen).

<img src="./multimedia/lego_mindstorms.png" width="100%" align="center">

<sup><sub>The LEGO Mindstorms Python interface</sub></sup>

* Once I have something more or less functional, I bring the big guns. Namely, I open a [Jupyter Notebook](https://jupyter.org/). Using [Jupytext](https://github.com/mwouts/jupytext), I configure my notebook (i.e., a `.ipynb` file) to be paired with a "percent Script". This generates a `.py` file which is linked to the original notebook.  

<img src="./multimedia/jupyter_notebook.png" width="100%" align="center">

<sup><sub>Configuring a Jupyter Notebook using Jupytext</sub></sup>

* Now, I can use [Spyder](https://www.spyder-ide.org/) (my preferred Python IDE) to indirectly work on the Jupyter Notebook. I copy the code from the LEGO Mindstorms app into the `.py` script. There, I can define text cells with `%% [markdown]` and code cells with `%%`.

<img src="./multimedia/spyder.png" width="100%" align="center">

<sup><sub>Working on Spyder</sub></sup>

* This is where the magic happens. Every time that I save the `.py` file, I can refresh the `.ipynb` file and see the changes there. This is a very elegant way to work on notebooks in a simple script, which as you can imagine is incredibly handy, since it allows me to create notebooks to explain the different steps of the programs in a nice format. For more details on how Jupytext works, I suggest you take a look at its [documentation](https://jupytext.readthedocs.io/en/latest/).

<img src="./multimedia/jupyter_notebook_2.png" width="100%" align="center">

<sup><sub>The Jupyter Notebook reflects the changes of the `.py` file.</sub></sup>

*  Lastly, I can just copy and paste the contents of the `.py` file into the LEGO Mindstorms app and it will work, since all the extra stuff (headers, cell definition) is defined as comments.

<img src="./multimedia/lego_mindstorms_2.png" width="100%" align="center">

<sup><sub>The LEGO Mindstorms Python interface with code from the `.py` file. It works!</sub></sup>


After this, I just get into the coding and documentation cycle (with a lot of copy-pasting in between). This setup isn't ideal, but at least it works. I hope that in the future the LEGO Mindstorms app works with `.py` files. Technically, Python support is still on beta, so it might still happen!

---------

**TLDR**: For each project, copy the contents of the `.py` file into the Mindstorms Python project.


## Questions? Feedback?
If you have any questions, comments, or feedback, please [open a discussion](https://github.com/arturomoncadatorres/lego-mindstorms/discussions). If there is a problem with the code (e.g., mistake), please [open an issue](https://github.com/arturomoncadatorres/lego-mindstorms/issues). Moreover, you can always drop me a line on [Twitter (@amoncadatorres)](https://twitter.com/amoncadatorres).
