# coding: utf-8

import random

def get_secret_num(num_digits):
    """
    Return a string that is num_digits long, made up of a unique random digits.
    """
    numbers = list(range(10))
    random.shuffle(numbers)
    secret_num = ''
    for i in range(num_digits):
        secret_num += str(numbers[i])
    return secret_num


def get_clues(guess, secret_num):
    """
    Return a string with the pico, fermi, bagels clues to the user.
    """
    if guess == secret_num:
        return 'You got it!'
    
    clue = []
    
    for i in range(len(guess)):
        if guess[i] == secret_num[i]:
            clue.append('Fermi')
        elif guess[i] in secret_num:
            clue.append('Pico')
    if len(clue) == 0:
        return 'Bagels'
    
    clue.sort()
    return ' '.join(clue)


def is_only_digits(num):
    """
    Return True if num is a string made up only of digits. Otherwise
    return False.
    """
    if num == '':
        return False
    
    for i in num:
        if i not in '0 1 2 3 4 5 6 7 8 9'.split():
            return False
        
    return True

def play_again():
    """
    Return True if the player wants to play again. Otherwise return
    False
    """
    print('Do you want to play again? (yes or no)')
    return input().lower().startswith('y')


NUMDIGITS = 3
MAXGUESS = 10

print('-   BAGELS   -')
print('I am think of a %s-digits number. Try to guess what it is.\n' % (NUMDIGITS))
print('Here are some clues:')
print('When I say:   That means:')
print('  Pico         One digit is correct but in the wrong position.')
print('  Fermi        One digit is correct and in the right position.')
print('  Bagels       No digit is correct')
print()

while True:
    secret_num = get_secret_num(NUMDIGITS)
    print('I have thought up a number. You have %s guesses to get it.\n' % (MAXGUESS))
    
    num_guesses = 1
    while num_guesses <= MAXGUESS:
        guess = ''
        while len(guess) != NUMDIGITS or not is_only_digits(guess):
            print('Guess #%s: ' % (num_guesses))
            guess = input()
        
        clue = get_clues(guess, secret_num)
        print(clue)
        num_guesses += 1
        
        if guess == secret_num:
            break
        if num_guesses > MAXGUESS:
            print('You ran out of guesses. The answer was %s.' % (secret_num))
    
    if not play_again():
        break