# This is 'impossible hangman', a hangman game that keeps changing the word until there is no possibility left.
# Try it out!

import re
import sys
import random

# Importing a list of 5-letter words. You can find this list in this same directory under 'words.txt'.
# Make sure to change the path in line 11.
five_letter_words = []
with open('/Users/Julian/Desktop/words.txt') as input_file:
    for line in input_file:
        if len(line) == 7:
            five_letter_words.append(line[0:5])


words = five_letter_words
first_solution = "-----"


# This function checks how many additional (!) letters the guess has in common with a word
def compare3(solution, word, guess):
    n = 0
    comp = zip(solution, word, guess)
    for i, j, k in comp:
        if i == "-" and j == k:
            n += 1
    return n


# This function takes the guess and updates the word list so that the game is as hard as possible within the constraints
def take_guess(word_list, solution):
    guess = raw_input("Guess a 5-letter word: \n").lower()
    if guess == "?":
        print(word_list)
    elif not re.match("^[a-z]*$", guess) or len(guess) != 5:
        print "Error. Only 5-letter words allowed (a-z). Try again! \n"
        take_guess(word_list, solution)
        sys.exit()
    lowest = float("inf")
    for x in word_list:
        score = compare3(solution, x, guess)
        if score < lowest:
            lowest = score
    if lowest == 0:
        new_words = [x for x in word_list if compare3(solution, x, guess) == 0]
        new_solution = solution
        print("You guessed " + str(lowest) + " letters correctly.")
        print(new_solution)
        take_guess(new_words, new_solution)
        sys.exit()
    else:
        new_words = [x for x in word_list if compare3(solution, x, guess) == lowest]
        new_solution = ""
        idx = random.randint(0, len(new_words) - 1)
        for i in xrange(len(solution)):
            if solution[i] != "-":
                new_solution = new_solution + solution[i]
            elif solution[i] == "-" and guess[i] == new_words[idx][i]:
                new_solution = new_solution + new_words[idx][i]
            else:
                new_solution = new_solution + "-"
        print("You guessed " + str(lowest) + " letters correctly.")
        print(new_solution)
        if new_solution == guess:
            print("Congrats! You guessed the right word. The solution is " + new_solution.upper())
            sys.exit()
        take_guess(new_words, new_solution)


def play_game():
    print("Welcome to HANGMAN IMPOSSIBLE! \nKeep guessing the word. If you get frustrated, type '?' to see a list of "
          "remaining words. Enjoy!\n\n")
    take_guess(words, first_solution)

play_game()
