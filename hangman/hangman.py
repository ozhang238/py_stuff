#!/usr/bin/python
import sys
from sys import stdin
import re
import string
import random

MAX_GUESS = 6
WORD_LIST = ['fish', 'salmon','trout','blueberry']

retry_prompt = """Do you want to play again?
Yes or No?"""

guess_prompt = """Guess a new letter.
You have {0} wrong guess(es) left.
Guesses must be a single letter of the alphabet"""

intro_msg = """H A N G M A N
Try to guess the letters of a secret word.
You can guess wrong {0} times"""
seperator = "------------------------------------------------------"
win_msg = "You WON! Congratulations!"
lose_msg = "You are a loser"

class HangmanState():
    def __init__(self, word, hint, maxGuess ):
        self.unguessed = set( list(string.ascii_lowercase) )
        self.guessed = set()
        self.word = word
        self.wordList = list(self.word)
        self.wordLetters = set(self.wordList)
        self.hint = hint 
        self.maxGuess = maxGuess 

    def update(self, guess): #guess being a char
        self.guessed.add(guess)
        self.unguessed.remove(guess)
        print("MATCH!" if guess in self.wordLetters else "WRONG")
    def wrongGuesses(self):
        return  [x for x in self.guessed.difference( self.wordLetters) ]
    
    def guessesLeft(self):
        return self.maxGuess - len(self.guessed.difference( self.wordLetters ) )
    def word_str(self):
        return " ".join( map( lambda x : x if x in self.guessed else "_", self.wordList ) )
    def isLose(self):
        return not self.guessesLeft() and not self.isWin()
    def isWin(self):
        return self.guessed.issuperset( self.wordLetters )
    def isDone(self):
        return self.isWin() or self.isLose()

    def __str__(self):
        return """Correct guess(es) : {0}
Incorrect guess(es) : {1}
Previous bad guesses : {2}
{3}{4}""".format( len( self.wordLetters.intersection( self.guessed ) ),
              len(self.wrongGuesses()),
              self.wrongGuesses(),
              "(hint={0})".format(self.word) if self.hint else "",
              self.word_str() ) 

def get_input():
    return stdin.readline().rstrip().lower()

def is_yes(s):
    return  s == "y" or s == "yes"

def get_retry():
    return is_yes(get_input())

def get_guess(unguessedLetters):
    guess = get_input()
    if ( len(guess) != 1 ):
        print("Guesses must be one character long.")
    elif (guess not in unguessedLetters):
        print("You already guessed {0}. Try another letter.".format(guess) )
    else:
        return guess
    return get_guess(unguessedLetters)

def play_hangman(max_guess, word, hint):
    print(intro_msg.format(max_guess))
    myState = HangmanState(word, hint, maxGuess = MAX_GUESS)
    while ( not myState.isDone() ):
        print(seperator)
        print(guess_prompt.format( myState.guessesLeft()) )
        myState.update( get_guess(myState.unguessed) )
        print(myState)

    print(seperator)
    if myState.isWin():
        print(win_msg)
    else:
        print(lose_msg)

def main(argv=None):
    retry = 1
    while (retry):
        play_hangman(MAX_GUESS, random.choice(WORD_LIST), hint=False )
        print(seperator)
        print(retry_prompt)
        retry = get_retry()

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))