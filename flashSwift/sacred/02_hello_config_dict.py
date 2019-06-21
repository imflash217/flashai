# coding=utf-8

"""
A configuable Hello World EXPERIMENT.
In this example, we configure the message using a dicionary with `ex.add_config` method
You can run it like this:

    $ ./02_hello_world_config_dict.py
    WARNING - 02_hello_config_dict - No observers have been added to this run
    INFO - 02__hello_config_dict - Running command 'main'
    INFO - 02_hello_config_dict - Started
    Hello world!
    INFO - 02_hello_config_dict - Completed after 0:00:00

This message can also be changed using the `with` command-line argument:

    $ ./02_hello_config_dict.py with message="Namaste World!!!"
    WARNING - 02_hello_config_dict - No observers have been added to this run
    INFO - 02_hello_config_dict - Running command 'main'
    INFO - 02_hello_config_dict - Started
    Namaste World!!!
    INFO - 02_hello_config_dict - Completed after 0:00:00
"""

from __future__ import division, print_function, unicode_literals
from sacred import Experiment

ex = Experiment()

# We add message to the configuration of the experiemnt here
ex.add_config({
    "message": "Hello World!!!!",
    "king": "Prithvi",
    "queen": "Sanyogita",
    })

# Notice, how we can access the mesage here by taking it as an argument
@ex.automain
def mainX(message, king, queen):
    print(f"{message} from {king} and {queen}")
















