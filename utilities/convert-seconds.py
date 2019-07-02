#python3

"""
Convert seconds to human-speak. I modified another example program I had written
  for a training class I took. This was to fulfill a challenge posed to me by a
  co-worker. It may not be the most elegant way to do it, and after I finished,
  I realized there might be a python library to do this. While I didn't find
  one, I did locate this page, which has some other interesting solutions.
  http://stackoverflow.com/questions/4048651/python-function-to-convert-seconds-into-minutes-hours-and-days
"""
debug = False

if debug == True:
    print ("minute: 60 seconds, hour: 3,600 seconds, day: 86,400 seconds")
    print ("week: 604,800 seconds, month (30 days): 2,592,000 seconds")
    print ("year (365 days): 31,536,000 seconds")
    print ("decade (365 days x 10): 315,360,000 seconds")
    print ("century (365 days x 10 x 10): 3,153,600,000 seconds")

while True:
    seconds_input = input('Enter the number of seconds, and I will convert it to real-time, or enter q to quit: ')
                                 
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
    second = 0
    
    try:
        seconds_input = int(seconds_input)
    except ValueError:
        print ("You entered " + str(seconds_input) + " . Either input a numeric value,or a q.")
        continue
        int(seconds_input)
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
            second = seconds_input
            if debug is True:
                print ("add minute. Input is now {}").format(seconds_input)
            minute += 1
            seconds_input = (seconds_input - 60)
            

    print ("Calculated to: "),
    if century > 0:
        print (str(century) + " centuries, and ")
    if decade > 0:
        print (str(decade) + " decades, and ")
    if year > 0:
        print (str(year) + " years, and ")
    if month > 0:
        print (str(month) + " months, and ")
    if week > 0:
        print (str(week) + " weeks, and ")
    if day > 0:
        print (str(day) + " days, and ")
    if hour > 0:
        print (str(hour) + " hours, and ")
    if minute > 0:
        print (str(minute) + " minutes, and")
    print (str(second) + " seconds")

print ("Aww, come back later!\n")
