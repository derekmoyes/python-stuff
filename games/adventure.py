import random

basementClosetDoor = "closed"
currentLocation = "basement"
debug = False
done = False
equipped = ""
gameHelp = "Use <verb> <noun> to do stuff. You can also look to repeat the description of your location."
greeting = """You awake in what appears to be the basement of your local pub.

Your head hurts and you seem to be alone.

As the only window appears painted over, you can't tell whether it's night or day.

Oh, and your watch seems to be missing.\n"""
nouns = ["cue", "door", "exit", "kitchen", "stairs", "window"]
verbs = ["climb", "close", "go", "grab", "look", "open", "put", "take"]
# new verbs: run, get, enter, drop

def clearScreen():
    print ("\n" * 100)
    return

def deathText():
    "deathText randomly picks a message to display when the player dies, and the game is over."
    action = ""
    deaths = ["Ow, that left a mark.",
              "Well, that certainly wasn't a good idea!",
              "That really hurt.",
              "Ow.",
              "Huh."]
#    padChars = ((11 - len(playerName))/2)
#    deathName = playerName
#    while (padChars > 0):
#        padChars -= 1
#        deathName = str(" " + deathName + " ")
    tombstone = """
        _.---,._,'
       /' _.--.<
         /'     `'
       /' _.---._____
       \.'   ___, .-'`
           /'    \\              .
         /'       `-.          -|-
        |                       |
        |                   .-'~~~`-.
        |                 .'         `.
        |                 |  R  I  P  |
        |                 |           |
        |                 |""" + str.center(playerName, 11) + "|" + """
         \              \\\\|           |//               jgs
   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
"""
    print(tombstone + random.choice(deaths) + " You are dead.")
    return

def failText():
    "failText randomly picks a (hopefully) funny message to display when a combination of verb+noun wouldn't make sense"
    fails = ["That wouldn't be prudent.",
             "Not a good idea!",
             "That would leave a mark.",
             "Really?"]
    print(random.choice(fails))
    return

clearScreen()
playerName = raw_input("Who goes there? (Enter your name) ")
print("Welcome to Adventure, " + playerName + "!\n")

print(greeting)
while not done:
    if currentLocation == "basement":
        locationtext = "You seem to be in the basement. You see stairs going " \
                       "up, a small window, and a door on the left."
        if equipped == "":
            locationtext = locationtext + " There is a broken pool cue here."
    if currentLocation == "basementCloset":
        locationtext = "You are now in the basement closet. There's a funny " \
                       "smell here. It's dark."
    if currentLocation == "pubHallway":
        locationtext = "You are in a small hallway. There are stairs leading " \
                       "down into the basement, and what looks like an exit " \
                       "to the kitchen."
    if currentLocation == "pubKitchen":
        locationtext = "You are now in what looks like the pub's kitchen. " \
                       "The pub must be closed, although the kitchen still " \
                       "smells like supper. There's an exit to the hallway, " \
                       "and a swinging door leads to the pub's Great Room."
    if currentLocation == "pubGreatRoom":
        locationtext = "The local"

    if equipped == "broken pool cue":
        locationtext = locationtext + " You are holding a broken pool cue."

    action = ""
    thing = ""
    command = raw_input("What do you do?\n>>> ")
    if debug == True: print(command)
    if (command == "" or command == "help" or command == "Help" or command == "help "):
        print(gameHelp)
        continue
    if command == "look":
        print(locationtext)
        continue
    words = command.split()
    for word in words:
        if word in verbs:
            action = word
            if action == "look":
                action = ""
                print(locationtext)
                continue
        if word in nouns:
            thing = word
        if word not in verbs and word not in nouns:
            print("I don't understand what " + word + " means, sorry!")
            continue

    if currentLocation == "basement":
        if action == "climb":
            if thing == "stairs":
                currentLocation = "pubHallway"
                print("You climb the stairs.")
                continue
            else:
                failText()
                continue
        if action == "close":
            if thing == "door":
                if basementClosetDoor == "open":
                    basementClosetDoor = "closed"
                    print("The door to the closet creaks loudly as you close "
                          "it behind you.")
                    continue
                else:
                    print("The door is already closed.")
            else:
                failText()
                continue
        if action == "go":
            if thing == "door":
                if basementClosetDoor == "open":
                    currentLocation = "basementCloset"
                    print("You carefully walk into the basement closet.")
                    continue
                else:
                    print("The door is closed, but it doesn't seem locked.")
                    continue
            if thing == "stairs":
                currentLocation = "pubHallway"
                print("You climb the stairs.")
                continue
            else:
                failText()
                continue
        if (action == "grab" or action == "take"):
            if thing == "cue":
                equipped = "broken pool cue"
                print("The broken pool cue in your hand makes you feel safer.")
                continue
            else:
                failText()
                continue
        if action == "open":
            if thing == "window":
                print("As it's painted shut, the window seems jammed.")
                continue
            if thing == "door":
                if basementClosetDoor == "closed":
                    basementClosetDoor = "open"
                    print("The door to the closet creaks loudly as you "
                          "slowly open it. It's very dark in there.")
                    continue
                else:
                    print("It's already open, silly!")
                    continue
            else:
                failText()
                continue

    if currentLocation == "basementCloset":
        if action == "close":
            if thing == "door":
                if basementClosetDoor == "open":
                    basementClosetDoor = "closed"
                    print("The door to the closet creaks loudly as you "
                          "close it behind you. It's very dark in here.")
                    continue
                else:
                    print("It's so dark in here the door must already be "
                          "closed.")
                    continue
        if action == "go":
            if basementClosetDoor == "open":
                currentLocation = "basement"
                print("You walk into the basement.")
                continue
            else:
                clearScreen()
                print("You fumble around in the dark and trip over the "
                      "smelly, dirty mop bucket and fall down.")
                deathText()
                done = True
        if action == "open":
            if thing == "window":
                print("You feel around a bit and don't locate any windows.")
                continue
            if thing == "door":
                if basementClosetDoor == "closed":
                    basementClosetDoor = "open"
                    print("The door to the closet creaks loudly as you slowly "
                          "open it. It's brighter out there.")
                    continue
                else:
                    print("It's already open, silly!")
                    continue

    if currentLocation == "pubHallway":
        if action == "climb":
            if thing == "stairs":
                currentLocation = "basement"
                print("You climb the stairs.")
                continue
            else:
                failText()
                continue
        if action == "go":
            if (thing == "exit" or thing == "kitchen"):
                currentLocation = "pubKitchen"
                clearScreen()
                print("You walk into the noisy kitchen and your eardrum "
                      "bursts due to the awful noise.")
                deathText()
                done = True
                continue
            if thing == "stairs":
                currentLocation = "basement"
                print("You climb the stairs.")
                continue
            else:
                failText()
                continue

    if currentLocation == "pubKitchen":
        if action == "go":
            if (thing == "hallway"):
                currentLocation = "pubHallway"
                print("You walk back into the hallway.")
                continue
            if thing == "exit":
                currentLocation = "pubGreatRoom"
                print("You exit the kitchen into the Great Room.")
                continue
            else:
                failText()
                continue
