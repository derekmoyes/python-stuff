#!/usr/bin/env python3
"""
Convert seconds to human-speak. I modified another example program I had
  written for a training class I took. This was to fulfill a challenge posed to
  me by a co-worker. It may not be the most elegant way to do it, and after I
  finished, I realized there might be a python library to do this. While I
  didn't find one, I did locate this page, which has some other interesting
  solutions.
  http://stackoverflow.com/questions/4048651/python-function-to-convert-seconds-into-minutes-hours-and-days
"""

debug=False
# Adjust these variables for your environment.
DebugString        = "==> DEBUG:"


if debug:
  print("""
    minute  : 60 seconds,
    hour    : 3,600 seconds,
    day     : 86,400 seconds,
    week    : 604,800 seconds,
    month   : 2,629,800 seconds,
    year    : 31,557,600 seconds,
    decade  : 315,576,000 seconds,
    century : 3,155,760,000 seconds
      """)


while True:
  seconds_input = input(
"""
Enter the number of seconds, and I will convert it to human readable
time, or the letter [Q/q] to quit: """
)

  if debug:
    print("%s Your input: %s" % (DebugString, seconds_input))

  if seconds_input == "q" or seconds_input == "Q":
    break

  century=0
  decade=0
  year=0
  month=0
  week=0
  day=0
  hour=0
  minute=0
  second=0
  buildoutput=""

  try:
    seconds_input = int(seconds_input)
  except ValueError:
    print("You entered %s. That's not a integer." % seconds_input)
    continue
    int(seconds_input)
  while seconds_input > 0:

    if seconds_input >= 3155760000:
      if debug:
        print("%s century" % DebugString)
      century += 1
      seconds_input = (seconds_input - 3155760000)

    if seconds_input > 315575999 and seconds_input <= 3155759999:
      if debug:
        print("%s decade" % DebugString)
      decade += 1
      seconds_input = (seconds_input - 315576000)

    if seconds_input > 31557599 and seconds_input <= 315575999:
      if debug:
        print("%s year" % DebugString)
      year += 1
      seconds_input = (seconds_input - 31557600)

    if seconds_input > 2629799 and seconds_input <= 31557599:
      if debug:
        print("%s month" % DebugString)
      month += 1
      seconds_input = (seconds_input - 2629800)

    if seconds_input > 604799 and seconds_input <= 2629799:
      if debug:
        print("%s week" % DebugString)
      week += 1
      seconds_input = (seconds_input - 604800)

    if seconds_input > 86399 and seconds_input <= 604799:
      if debug:
        print("%s day" % DebugString)
      day += 1
      seconds_input = (seconds_input - 86400)

    if seconds_input > 3599 and seconds_input <= 86399:
      if debug:
        print("%s hour" % DebugString)
      hour += 1
      seconds_input = (seconds_input - 3600)

    if seconds_input > 59 and seconds_input <= 3599:
      if debug:
        print("%s minute" % DebugString)
      minute += 1
      if debug:
        print("%s Minute: %s" % (DebugString, minute))
        print("%s Subtracting one minute..." % DebugString)
      if seconds_input > 0:
        seconds_input = (seconds_input - 60)

    if seconds_input > 0 and seconds_input <= 59:
      if debug:
        print("%s Second: %s" % (DebugString, second))
        print("%s Setting seconds..." % DebugString)
        print("%s Subtracting 60 seconds..." % DebugString)
      second = seconds_input
      seconds_input = (seconds_input - 60)


  if century > 0:
    buildoutput = (str(century) + " centuries, ")
  if decade > 0:
    buildoutput = buildoutput + (str(decade) + " decades, ")
  if year > 0:
    buildoutput = buildoutput + (str(year) + " years, ")
  if month > 0:
    buildoutput = buildoutput + (str(month) + " months, ")
  if week > 0:
    buildoutput = buildoutput + (str(week) + " weeks, ")
  if day > 0:
    buildoutput = buildoutput + (str(day) + " days, ")
  if hour > 0:
    buildoutput = buildoutput + (str(hour) + " hours, ")
  if minute > 0:
    buildoutput = buildoutput + (str(minute) + " minutes, ")
  if second == 1:
    buildoutput = buildoutput + (str(second) + " second")
    second = -42
  if second == 0 or second > 0:
    buildoutput = buildoutput + (str(second) + " seconds")
  print("Calculated to: %s." % buildoutput)

print("Aww, come back later!\n")
