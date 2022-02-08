#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Convert temperature from Fahrenheit to Celsius and back again.
https://reference.yourdictionary.com/resources/what-s-the-easiest-way-to-convert-fahrenheit-to-celsius.html
"""

debug = False
# Adjust these variables for your environment.
DebugString = "==> DEBUG:"

if debug:
    print("""
        %s Converting F to C can be done using the estimate way, F-30/2, or the precise way, F-30/1.8.
        """.format(DebugString))

# Start.
print("I convert temperatures.")

# Loop until quit.
while True:
    temp_input = input("Enter the temperature, as an integer or decimal, or the letter [Q/q] to quit: ")

    if debug:
        print("{} Your input: {}".format(DebugString, temp_input))

    if temp_input == "q" or temp_input == "Q":
        break

# Ensure we have an integer, handle if necessary.
#  try:
#    seconds_input = int(seconds_input)
#  except ValueError:
#    print("You entered %s. That's not a integer." % seconds_input)
#    continue
#    int(seconds_input)

# Perform the conversions, assume F => C at this point.
    convert_me = float(temp_input)
    if debug:
        print("{} Converted your input to a float (decimal): {}".format(DebugString, convert_me))

    temp_estimate = (convert_me - 30) / 2
    temp_precise = (convert_me - 30) / 1.8

# Output.
    print("Celsius temperature estimated {}°,\n"
          "                       actual {}°.".format(round(temp_estimate, 2), round(temp_precise, 2)))

# Quit when q or Q is entered.
print("Aww, come back later!\n")
