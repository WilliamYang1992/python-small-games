# coding: utf-8

import random

def draw_board(board):
    """
    Print out the board that it was passed.
    "board" is a list of 10 strings representing the board(ignore index 0).
    """
    print('   |   |')
    print(' {0} | {1} | {2}'.format(board[7], board[8], board[9]))
    print('   |   |')
    print(' 7   8   9')
    print('-----------')
    print('   |   |')
    print(' {0} | {1} | {2}'.format(board[4], board[5], board[6]))
    print('   |   |')
    print(' 4   5   6')
    print('-----------')
    print('   |   |')
    print(' {0} | {1} | {2}'.format(board[1], board[2], board[3]))
    print('   |   |')
    print(' 1   2   3')
    
    
def input_player_letter():
    """
    Let the player type which letter they want to be.
    Returns a list with the player's letter as the first item, and the computer's
    letter as the second.
    """
    letter = ''
    while not (letter == 'X' or letter == 'O'):
        print('Do you want to be X or O?')
        letter = input().upper()
    
    if letter == 'X':
        return ['X', 'O']
    else:
        return ['O', 'X']
    

def who_goes_first():
    if random.randint(0, 1):
        return 'player'
    else:
        return 'computer'


def play_again():
    """
    Return True if the player wants to play again, otherwise it returns False.
    """
    print('Do you want to play again? (yes or no)')
    return input().lower().startswith('y')


def make_move(board, letter, move):
    board[move] = letter


def is_winner(board, letter):
    """
    Return True if the player has won.
    """
    bo = board
    le = letter
    return (bo[7] == le and bo[8] == le and bo[9] == le) \
           or (bo[4] == le and bo[5] == le and bo[6] == le) \
           or (bo[1] == le and bo[2] == le and bo[3] == le) \
           or (bo[7] == le and bo[4] == le and bo[1] == le) \
           or (bo[8] == le and bo[5] == le and bo[2] == le) \
           or (bo[9] == le and bo[6] == le and bo[3] == le) \
           or (bo[1] == le and bo[2] == le and bo[3] == le) \
           or (bo[7] == le and bo[5] == le and bo[3] == le) \
           or (bo[9] == le and bo[5] == le and bo[1] == le)


def get_board_copy(board):
    """Return a duplicate of the board list"""
    dupe_board = board[:]
    return dupe_board


def is_space_free(board, move):
    """
    Return True if the passed move is free on the passed board.
    """
    return board[move] == ' '
    

def get_player_move(board):
    """
    Let the player type in their move.
    """
    move = ''
    while move not in '1 2 3 4 5 6 7 8 9'.split() or \
          not is_space_free(board, int(move)):
        print('What is your next move? (1-9)')
        move = input()
    return int(move)


def choose_random_move_from_list(board, moves_list):
    """
    Return a valid move from the passed list on the passed board.
    Return None if there is no valid move.
    """
    possible_moves = []
    for i in moves_list:
        if is_space_free(board, i):
            possible_moves.append(i)
    
    if len(possible_moves) != 0:
        return random.choice(possible_moves)
    else:
        return None
    

def get_computer_move(board, computer_letter):
    """
    Determine where to move and return that move.
    """
    if computer_letter == 'X':
        player_letter = 'O'
    else:
        player_letter = 'X'
    
    # First, check if computer can win in the next move.
    for i in range(1, 10):
        copy = get_board_copy(board)
        if is_space_free(copy, i):
            make_move(copy, computer_letter, i)
            if is_winner(copy, computer_letter):
                return i
            
    # Check if the player can win on their next move, and block them.
    for i in range(1, 10):
        copy = get_board_copy(board)
        if is_space_free(copy, i):
            make_move(copy, player_letter, i)
            if is_winner(copy, player_letter):
                return i
    
    # Try to take one of the corners, if they are free.
    move = choose_random_move_from_list(board, [1, 3, 7, 9])
    if move != None:
        return move
    
    # Try to take the center, if it is free.
    if is_space_free(board, 5):
        return 5
    
    # Move on one of the sides.
    return choose_random_move_from_list(board, [2, 4, 6, 8])


def is_board_full(board):
    """
    Return True if every space on the board has been taken.
    Otherwise return false.
    """
    for i in range(1, 10):
        if is_space_free(board, i):
            return False
    return True

print('Welcome to Tic Tac Toe!')

while True:
    # Reset the board
    the_board = [' '] * 10
    player_letter, computer_letter = input_player_letter()
    turn = who_goes_first()
    print('The {0} will go first.'.format(turn))
    game_is_playing = True
    
    while game_is_playing:
        if turn == 'player':
            # Player's turn.
            draw_board(the_board)
            move = get_player_move(the_board)
            make_move(the_board, player_letter, move)
            
            if is_winner(the_board, player_letter):
                draw_board(the_board)
                print('Hooray! You have won the game!')
                game_is_playing = False
            else:
                if is_board_full(the_board):
                    draw_board(the_board)
                    print('The game is a tie!')
                    break
                else:
                    turn = 'computer'
        else:
            # Computer's turn.
            move = get_computer_move(the_board, computer_letter)
            make_move(the_board, computer_letter, move)
            
            if is_winner(the_board, computer_letter):
                draw_board(the_board)
                print('The computer has beaten you! You lose.')
                game_is_playing = False
            else:
                if is_board_full(the_board):
                    draw_board(the_board)
                    print('The game is a tie!')
                    break
                else:
                    turn = 'player'
    
    if not play_again():
        break

