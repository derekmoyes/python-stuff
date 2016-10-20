"""
Convert seconds to human-speak
"""
debug = False

if debug == True:
    print "minute: 60 seconds"
    print "hour: 3,600 seconds"
    print "day: 86,400 seconds"
    print "week: 604,800 seconds"
    print "month (30 days): 2,592,000 seconds"
    print "year (365 days): 31,536,000 seconds"
    print "decade (365 days x 10): 315,360,000 seconds"
    print "century (365 days x 10 x 10): 3,153,600,000 seconds"

while True:
    seconds_input = raw_input('\nEnter the number of seconds, and I will '
                              'convert it to real-time,\nor enter q to quit: ')
    if seconds_input == "q" or seconds_input == "Q":
        break

    century = 0
    decade = 0
    year = 0
    month = 0
    week = 0
    day = 0
    hour = 0
    minute = 0

    try:
        seconds_input = int(seconds_input)
    except ValueError:
        print "You entered {}. Either input a numeric value, " \
              "or a q.".format(seconds_input)
        continue

    while seconds_input > 0:
        if seconds_input > 3153599999:
            century += 1
            seconds_input = (seconds_input - 3153599999)
        if seconds_input > 315359999 and seconds_input <= 3153599999:
            decade += 1
            seconds_input = (seconds_input - 315359999)
        if seconds_input > 2591999 and seconds_input <= 315359999:
            year += 1
            seconds_input = (seconds_input - 2591999)
        if seconds_input > 604799 and seconds_input <= 2591999:
            month += 1
            seconds_input = (seconds_input - 604799)
        if seconds_input > 86399 and seconds_input <= 604799:
            week += 1
            seconds_input = (seconds_input - 86399)
        if seconds_input > 3599 and seconds_input <= 86399:
            day += 1
            seconds_input = (seconds_input - 3599)
        if seconds_input > 60 and seconds_input <= 3599:
            hour += 1
            seconds_input = (seconds_input - 60)
        if seconds_input <= 59:
            if debug is True:
                print "add minute. Input is now {}".format(seconds_input)
            minute += 1
            seconds_input = (seconds_input - 60)

    print "Calculated to: ",
    if century > 0:
        print "{} centuries, and ".format(century),
    if decade > 0:
        print "{} decades, and ".format(decade),
    if year > 0:
        print "{} years, and ".format(year),
    if month > 0:
        print "{} months, and ".format(month),
    if week > 0:
        print "{} weeks, and ".format(week),
    if day > 0:
        print "{} days, and ".format(day),
    if hour > 0:
        print "{} hours, and ".format(hour),
    if minute > 0:
        print "{} minutes".format(minute),

print "Aww, come back later!\n"