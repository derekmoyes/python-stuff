"""
Hangman example generated by ChatGPT, 2024
"""

import random


def select_word():
    word_list = ["apple", "banana", "cherry", "date", "elderberry", "fig", "grape", "honeydew", "imbe", "jackfruit"]
    return random.choice(word_list)


def update_word(word, guessed_letters):
    masked_word = ""
    for letter in word:
        if letter in guessed_letters:
            masked_word += letter
        else:
            masked_word += "_"
    return masked_word


def hangman():
    tries = 6
    word = select_word()
    guessed_letters = []

    print("Welcome to Hangman!")
    print("Guess the letters of the word. You have 6 tries.")

    while tries > 0:
        print("\nWord:", update_word(word, guessed_letters))
        print("Tries remaining:", tries)

        guess = input("Enter a letter: ").lower()

        if guess in guessed_letters:
            print("You already guessed that letter. Try again.")
            continue

        guessed_letters.append(guess)

        if guess not in word:
            tries -= 1
            print("Incorrect guess!")

            if tries == 0:
                print("You lost! The word was:", word)
        else:
            masked_word = update_word(word, guessed_letters)
            if masked_word == word:
                print("Congratulations! You won!")
                break

    play_again = input("Do you want to play again? (yes/no): ").lower()
    if play_again == "yes":
        hangman()
    else:
        print("Thank you for playing Hangman!")


hangman()
