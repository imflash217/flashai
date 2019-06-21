# coding=utf-8

"""

"""

from __future__ import division, print_function, unicode_literals
from sacred import Experiment

# create an experiemnt and name it
ex = Experiment("hello_config_scope")

# A ConfigScope is a function decorated with @ex.config
# All variables of this function will be put into the configuration

@ex.config
def cfg(_log):
    greeting = "Hello"
    recepient = "Prithvi"
    message = f"{greeting}\! {recepient}"


# We can access all the variables in function with @ex.config decoration
@ex.automain
def main(message):
    print(message)      # OKAY
    print(greeting)     # ERROR: greeting is not passed to the enclosing method

