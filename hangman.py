# coding: utf-8

import random

HANGMANPICS = [
    """
    +---+
    |   |
        |
        |
        |
        |
  ========
    """,
    """
    +---+
    |   |
    O   |
        |
        |
        |
  ========
    """,
    """
    +---+
    |   |
    O   |
   /    |
        |
        |
  ========
    """,
    """
    +---+
    |   |
    O   |
   /|   |
        |
        |
  ========
    """,
    """
    +---+
    |   |
    O   |
   /|\  |
        |
        |
  ========
    """,
    """
    +---+
    |   |
    O   |
   /|\  |
   /    |
        |
  ========
    """,
    """
    +---+
    |   |
    O   |
   /|\  |
   / \  |
        |
  ========
    """,
    """
    +---+
    |   |
   [O   |
   /|\  |
   / \  |
        |
  ========
    """,
    """
    +---+
    |   |
   [O]  |
   /|\  |
   / \  |
        |
  ========
    """
]

words = {
    'Colors': 'red orange yellow green blue indigo violet white black brown purple pink'.split(),
    'Sports': 'swimming running basketball tennis badminton soccer volleyball athletics'.split(),
    'Fruits': 'apple banana peach pineapple orange watermelon grape pear cherry cantaloupe'.split(),
    'Animals': 'bear bat zebra panda monkey dog owl rabbit tiger sheep lion turtle whale.'.split(), 
}

def get_random_word(word_dict):
    """Returns a random string from the passed list of strings."""
    word_key = random.choice(list(word_dict.keys()))
    word_index = random.randint(0, len(word_dict[word_key]) - 1)
    return word_dict[word_key][word_index], word_key


def display_board(HANGMANPICS, missed_letters, correct_letters, secret_word):
    print(HANGMANPICS[len(missed_letters)])
    print()
    
    print('Missed letters:', end=' ')
    for letter in missed_letters:
        print(letter, end=' ')
    print()
    
    blanks = '_' * len(secret_word)
    
    for i in range(len(secret_word)):
        if secret_word[i] in correct_letters:
            blanks = blanks[:i] + secret_word[i] + blanks[i+1:]
    
    for letter in blanks:
        print(letter, end=' ')
    print()
    

def get_guess(already_guessed):
    """
    Return the letter the player entered. This function makes user the 
    player entered a single letter, and not something else.
    """
    while True:
        print('Guess a letter.')
        guess = input()
        guess = guess.lower()
        if len(guess) != 1:
            print('Please enter a single letter.')
        elif guess in already_guessed:
            print('You have already guessed that letter. Choose again.')
        elif guess not in 'abcdefghijklmnopqrstuvwxyz':
            print('Please enter a LETTER.')
        else:
            return guess


def play_again():
    """
    Returns True if the player wants to play again,
    otherwise it returns false.
    """    
    print('Do you want to play again? (yes or no)')
    return input().lower().startswith('y')


print('- H A N G M A N -')
missed_letters = ''
correct_letters = ''
secret_word, secret_key = get_random_word(words)
game_is_done = False

while True:
    print('The secret word is in the set: {0}'.format(secret_key))
    display_board(HANGMANPICS, missed_letters, correct_letters, secret_word)
    guess = get_guess(missed_letters+correct_letters)
    
    if guess in secret_word:
        correct_letters = correct_letters + guess
        
        found_all_letters = True
        for i in range(len(secret_word)):
            if secret_word[i] not in correct_letters:
                found_all_letters = False
                break
        if found_all_letters:
            print('YES! The secret word is {0}! You have won!'.format(secret_word))
            game_is_done = True
    else:
        missed_letters = missed_letters + guess
        # Check if player has guesses too many times and lost
        if len(missed_letters) == len(HANGMANPICS) - 1:
            display_board(HANGMANPICS, missed_letters, correct_letters, secret_word)
            print('You have run out of guesses!\nAfter {0} missed guesses and {1} correct guesses, the word '
                  'was {2}'.format(len(missed_letters), len(correct_letters), secret_word))
            game_is_done = True
    
    # Ask the player if they want to play again (but only if the game is done)
    if game_is_done:
        if play_again():
            missed_letters = ''
            correct_letters = ''
            game_is_done = False
            secret_word, secret_key = get_random_word(words)
        else:
            break
            
    