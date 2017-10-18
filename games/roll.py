#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Simple dice roller example.

Python 2.7 PEP8 game
"""

import random
import sys


min = 1
max = 6

roll_again = "yes"

while roll_again == "yes" or roll_again == "y":
    roller = int(raw_input("How many dice should I roll? "))
    print("Rolling the dice...")
    print("Let me roll those " + str(roller) + " dice for you!")
    print("The values are...")
    while roller > 0:
        value = (random.randint(min, max))
        sys.stdout.write(str(value) + ", ")
        roller -= 1

    roll_again = str.lower(raw_input("\nRoll the dice again? "))
