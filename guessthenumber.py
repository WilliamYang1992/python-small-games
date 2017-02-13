# coding: utf-8

# This is a "Guess the number" game.
# 这是一个猜数字的游戏

import random

# Settings
# 设置参数
max_number = 100
guesses_taken = 0
max_guesses_taken = 6

print('Hello! What is your name?')
my_name = input()

number = random.randint(1, max_number)
print('Well, {0}, I am thinking of a number between 1 and {1}.'.format(my_name, max_number))

while guesses_taken < max_guesses_taken:
    print('Take a guess.')
    guess = int(input())
    guesses_taken += 1
    
    if guess < number:
        print('Your guess is too low.')
    elif guess > number:
        print('Your guess is too high.')
    else:
        break

if guess == number:
    print('Good job, {0}! You guessed my number in {1} guesses!'.format(my_name, guesses_taken))
else:
    print('Nope. The number I was thinking of was {0}.'.format(number))