#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Simple dice roller example.

Python 2.7 PEP8 game
"""

import random
min = 1
max = 6

roll_again = "yes"

while roll_again == "yes" or roll_again == "y":
    print("Rolling the dice...")
    print("The values are...")
    print(random.randint(min, max))
    print(random.randint(min, max))

    roll_again = raw_input("Roll the dice again? ")
