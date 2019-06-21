# codng=utf-8

from __future__ import print_function, division, unicode_literals
from sacred import Experiment

ex = Experiment("commands")

@ex.config
def cfg():
    name="Prithvi"

@ex.command
def greet(name):
    """
    Print a nice greet message.
    uses the name from config.
    """
    print(f"Hello {name}! Nice to greet you!...")

@ex.command
def shout():
    """
    Shout slang question for "What is up???"
    """
    print("WHAAAAAZZZZUUUUUUPPPPP!!!!?????")

@ex.automain
def main():
    print("This is just the main command. Try greet or shout")
