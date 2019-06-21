# coding=utf-8

from __future__ import print_function, division, unicode_literals
from sacred import Experiment

ex = Experiment("randomness")
ex2 = Experiment("randomness2")

@ex.config
def cfg():
    reverse = False
    numbers = 1

@ex2.config
def cfg():
    reverse = True
    numbers = 2

@ex.capture
def do_random_stuff(numbers, _rnd):
    print([_rnd.randint(1, 100) for _ in range(numbers)])

@ex.capture
def do_more_random_stuff(_seed):
    print(_seed)

@ex2.capture
def do_random_stuff2(numbers, _rnd, _seed):
    print([_rnd.randint(100, 200) for _ in range(numbers)])
    print(_seed)



@ex.automain
def run(reverse):
    if reverse:
        do_more_random_stuff()
        do_random_stuff()
        do_random_stuff()
    else:
        do_random_stuff()
        do_random_stuff()
        do_more_random_stuff()

    do_random_stuff()

@ex2.automain
def run(reverse):
    if reverse:
        print(f"Reversing")
        do_random_stuff2()
    else:
        print(f"No reversing")
        # do_random_stuff2()

