# coding=utf-8

from __future__ import print_function, division, unicode_literals
from sacred import Experiment

ex = Experiment("captured_functions")

message = "This is global message"

@ex.config
def cfg(_log):
    global message
    message = "This is printed by function {}"

# Captured functions have access to all the configuration parameters

@ex.capture
def foo(message):
    print(message.format("foo"))

@ex.capture
def bar(message):
    print(message.format("bar"))

@ex.automain
def main():
    foo()   # NOTICE: We don't pass any argument here
    print(message)
    message = "Changed the mesage before.....{}"
    print(message)
    bar()   # NOTICE: or here!!!
            # NOTICE: But, we can call with arguments if we like it
    foo("Overriding the default message for {}")

