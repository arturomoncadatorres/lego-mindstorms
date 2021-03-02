<p align="center">
  <img width="100%" src="./multimedia/mindstorms_51515_logo.png">
</p>

------
<p align="center">
  <a href="#projects">Projects</a> •
  <a href="#my-programming-setup">My programming setup</a> •
  <a href="#additional-resources">Additional resources</a> •
  <a href="#questions-feedback">Questions/Feedback</a>
</p>

------

## Projects
All of the projects use the electronics of the [51515 set](https://www.lego.com/en-us/product/robot-inventor-51515) and are programmed using (Micro)Python (although some of them might include their Scratch equivalent). I've grouped them in three categories:

### [Base projects](https://github.com/arturomoncadatorres/lego-mindstorms/tree/main/base)<br>
* The [LEGO Mindstorms 51515 software](https://www.microsoft.com/en-us/p/lego-mindstorms-robot-inventor/9mtq0n7w1d6x) already comes with several programs for the different robots. However, these are programmed using Scratch. In this directory you will find their counterparts in Python.

<p align="center">
  <img width="90%" src="./multimedia/mindstorms_51515_robots.png">
</p>

### [Example scripts](https://github.com/arturomoncadatorres/lego-mindstorms/tree/main/examples)<br>
* A few example scripts that I've created to test or experiment some functionality that I thought would be worth sharing.

<table><tr>
<td> <img src="./examples/multimedia/azure.jpeg" alt="" style="width: 100%;"/> </td>
<td> <img src="./examples/multimedia/blue.jpeg" alt="" style="width: 100%;"/> </td>
<td> <img src="./examples/multimedia/cyan.jpeg" alt="" style="width: 100%;"/> </td>
<td> <img src="./examples/multimedia/green.jpeg" alt="" style="width: 100%;"/> </td>
<td> <img src="./examples/multimedia/orange.jpeg" alt="" style="width: 100%;"/> </td>
</tr>
<tr>
<td> <img src="./examples/multimedia/pink.jpeg" alt="" style="width: 100%;"/> </td>
<td> <img src="./examples/multimedia/red.jpeg" alt="" style="width: 100%;"/> </td>
<td> <img src="./examples/multimedia/violet.jpeg" alt="" style="width: 100%;"/> </td>
<td> <img src="./examples/multimedia/yellow.jpeg" alt="" style="width: 100%;"/> </td>
<td> <img src="./examples/multimedia/white.jpeg" alt="" style="width: 100%;"/> </td>
</tr>
</table>




### [MOCs](https://github.com/arturomoncadatorres/lego-mindstorms/tree/main/mocs)<br>
* Here I've documented my own creations (MOCs). For each of them, I've included the building instructions for the robot (as a PDF), as well as its corresponding (Python) program, so that anyone can reproduce them and, most importantly, *build* upon them!*

<p align="center">
  <img width="50%" src="./mocs/aat_ms5/multimedia/aat_ms5.png">
</p>

<sup><sub>* Pun absolutely intended</sup></sub>

-------

## My programming setup
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

##### <br> **TLDR**: For each project, copy the contents of the `.py` file into the Mindstorms Python project.

-------

## Additional resources
If you need some pointers on where to start learning Python to program your first LEGO Mindstorms robots or if you want to go deep into the rabbit hole with your creations, I recommend taking a look at this resources:
### Basics

* [Python programming lessons](https://primelessons.org/en/Lessons.html) by Sanjay and Arvind Seshan <br>
Amazing resource for LEGO Mindstorms robot programming. A bit focused towards FIRST LEGO League, but useless nevertheless. Content is structured as classroom lessons. It is actively being developed.

* [LEGO Mindstorms 51515 Micropython programming tutorial](https://www.eurobricks.com/forum/index.php?/forums/topic/181083-lego-mindstorms-51515-micropython-programming-tutorial/) by Coder Shah <br>
Handy playlist with some YouTube videos that should get you started quite quickly on the basics of Python for LEGO Mindstorms.

### Intermediate
* [LEGO Mindstorms FAQ](https://github.com/maarten-pennings/Lego-Mindstorms/blob/main/ms4/faq.md) by Maarten Pennings <br>
More than a FAQ, I'd say this is a guide well worth reading from start to bottom. Even if you already know the basics, I am sure you will learn something useful

* [(Unofficial) Documentation for LEGO Mindstorms Python API](https://onedrive.live.com/?authkey=%21AJZ35NPPkkN0Wfw&id=CD7CB52696D0FB0B%2150790&cid=CD7CB52696D0FB0B) by [Laid Back Koala](https://www.eurobricks.com/forum/index.php?/forums/topic/182548-some-ris-51515-docs/) <br>
Very handy resource if you are sick of the Knowledge Base closing every time you switch windows wrapped. It comes in a cohesive, nice PDF format. It also has a PDF for Scratch!

* [Undocumented Python for LEGO Mindstorms](https://antonsmindstorms.com/2021/01/14/advanced-undocumented-python-in-spike-prime-and-mindstorms-hubs/) by Anton's Mindstorms <br>
`from mindstorms import MSHub` and then `hub = MSHub()`, right? Well, actually `import hub` has way many more options. Spoiler alert: it is cool, but it is a tad less user friendly.

### Advanced
* [Pybricks](https://docs.pybricks.com/en/latest/) by the Pybricks team <br>
If you feel that the LEGO Mindstorms vanilla (Micro)Python starts being insufficient for your creations, you might want to take a look at Pybricks. Basically, you download a new firmware to your hub where you run Pybrick's version of (Micro)Python. However, note that [support for the 51515 set is still on alpha](https://github.com/pybricks/support/issues/167) at the time of writing.

* How can I run two motors asynchronously? <br>
The moment you start building more ellaborate robots, you will come across this issue sooner or later. So far, I've found two different ways to tackle this:
    - [Using co-routines](https://community.legoeducation.com/discuss/viewtopic/66/110), as proposed by David Lechner (actual code [here](https://gist.github.com/dlech/fa48f9b2a3a661c79c2c5880684b63ae)). I tried this approach in [Charlie's `drum_solo`](https://github.com/arturomoncadatorres/lego-mindstorms/tree/main/base/charlie) activity and it works quite well.
    - [Using mathematical functions](https://www.antonsmindstorms.com/2021/01/27/python-motor-synchronization-coordinating-multiple-spike-or-mindstorms-motors/), as proposed by Anton's Mindstorms. It looks quite ingenious. However, I haven't had the chance to try it myself.


----------

## Questions? Feedback?
If you have any questions, comments, or feedback, please [open a discussion](https://github.com/arturomoncadatorres/lego-mindstorms/discussions). If there is a problem with the code (e.g., mistake), please [open an issue](https://github.com/arturomoncadatorres/lego-mindstorms/issues). Moreover, you can always drop me a line on Twitter [(@amoncadatorres)](https://twitter.com/amoncadatorres).
