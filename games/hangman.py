"""
Simple hangman example. Added a word list, but only for *nix at this time.
"""

import random

debug = False

# Load the word list (*nix method) https://stackoverflow.com/questions/18834636/random-word-generator-python
word_file = "/usr/share/dict/words"
words = open(word_file).read().splitlines()
# Ignore any words that start with uppercase letters.
lower_words = [word for word in words if word[0].islower()]

if debug == True:
    # Print the word list, for debugging...
    x = 0
    for w in lower_words:
        # trying to find a way to remove apostrophe and accént aigu. I'm not sure if this is where it needs to go 
        # but when I run in debug it seems to work.
        print(str(w).replace("'b","").replace("'","").replace("é","e"))
        x += 1

# Count the number of words, so that we can choose one.
max = len(lower_words)
print("I'm hangman, and I currently know", max, "words.")

# Welcome the user.
name = input("What is your name? ")

# Set the secret word, by picking a random number between 1 and the max word loaded.
value = (random.randint(1, max))
word = lower_words[value]

if debug == True:
    # Print the secret word for debugging...
    print(word)
print("I've selected a random word from the dictionary,", name + ". Time to play!\n")

# This is the list of guesses the user will enter.
guesses = ''

# Set the number of turns.
turns = 10

while turns > 0:
    # Counter
    failed = 0
    # Check word.
    for char in word:
        if char in guesses:
            print(char, " ", end='');
        else:
            print("- ", end='');
            failed += 1

    if failed == 0:
        print("\n", name, "you won! The word was", word + "!")
        # Exit the script early if the user wins.
        break

    if len(guesses) > 0:
        print("\nSo far, you've guessed the following letters:", guesses)
        print("You have", + turns, "guesses left.")

    guess = input("\nGuess a character: ")

    if len(guess) > 1:
        guess = ""
        turns -= 1
        print("Hey, no cheating! Enter only one letter at a time.")
        print("You have", + turns, "guesses left.")

    guesses += guess
    guesses = sorted(guesses)

    if guess not in word:
        turns -= 1
        print("\nSorry,", guess, "is not in the word.\n")
        if turns == 0:
            print(name, ", you lost!\nThe word you were looking for was", word + "!")
