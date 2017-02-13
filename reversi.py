# -*- coding: utf-8 -*-

import sys
import random

try:
    import colorama
    use_color = True
except(ImportError):
    use_color = False


def draw_board(board):
    """
    Prints out the board that it was passed.Returns None.
    """
    HLINE = '  +----+----+----+----+----+----+----+----+'
    VLINE = '  |    |    |    |    |    |    |    |    |'
    print('    1    2    3    4    5    6    7    8')
    print(HLINE)
    for y in range(8):
        #print(VLINE)
        print(y+1, end=' ')
        for x in range(8):
            if len(str(board[x][y])) >= 2:
                print('| %s' % (board[x][y]), end=' ')
            else:
                print('| %s ' % (board[x][y]), end=' ')
        print('| ', end='')
        print(y+1)
        #print(VLINE)
        print(HLINE)
    print('    1    2    3    4    5    6    7    8')


def reset_board(board):
    """
    Blanks out the board it is passed, except for the original starting
    position.
    """
    for x in range(8):
        for y in range(8):
            board[x][y] = ' '
    
    # Starting pieces:
    board[3][3] = 'X'
    board[3][4] = 'O'
    board[4][3] = 'O'
    board[4][4] = 'X'
    

def get_new_board():
    """
    Creates a brand new, blank board data structure.
    """
    board = []
    for i in range(8):
        board.append([' '] * 8)
    return board


def is_on_board(x, y):
    """
    Return True if the coordinates are loacated on the board.
    """
    return x >= 0 and x <= 7 and y >= 0 and y <= 7


def is_valid_move(board, tile, xstart, ystart):
    """
    Return False if the player's move on space xstart, ystart is invalid.
    If it is a valid move, returns a list of spaces that would become the player's
    if they made a move here.
    """
    if board[xstart][ystart] != ' ' or not is_on_board(xstart, ystart):
        return False
    
    # Temporarily set the tile on the board.
    board[xstart][ystart] = tile
    
    if tile == 'X':
        other_tile = 'O'
    else:
        other_tile = 'X'
        
    tiles_to_flip = []
    for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1],
                                   [-1, -1], [-1, 0], [-1, 1]]:
        x, y = xstart, ystart
        x += xdirection  # First step in the direction.
        y += ydirection  # First step in the direction.
        if is_on_board(x, y) and board[x][y] == other_tile:
            # There is a piece belonging to the other player next to our piece.
            x += xdirection
            y += ydirection
            if not is_on_board(x, y):
                continue
            while board[x][y] == other_tile:
                x += xdirection
                y += ydirection
                if not is_on_board(x, y):
                    # Break out of while loop, then continue in for loop.
                    break
            if not is_on_board(x, y):
                continue
            if board[x][y] == tile:
                # There are pieces to flip over. Go in the reverse direction until we
                # reach the original space, nothing all the tiles along the way.
                while True:
                    x -= xdirection
                    y -= ydirection
                    if x == xstart and y == ystart:
                        break
                    tiles_to_flip.append([x, y])
    
    # Restore the empty space.
    board[xstart][ystart] = ' '
    # If no tiles were flipped, this is not a valid move.
    if len(tiles_to_flip) == 0:
        return False
    return tiles_to_flip


def get_board_copy(board):
    """
    Returns a duplicate of the board list.
    """
    dupe_board = get_new_board()
    for x in range(8):
        for y in range(8):
            dupe_board[x][y] = board[x][y]
    return dupe_board


def get_valid_moves(board, tile):
    # Return a list of [x,y] lists of valid moves for the given player on
    # the given board.
    valid_moves = []
    
    for x in range(8):
        for y in range(8):
            if is_valid_move(board, tile, x, y):
                valid_moves.append([x, y])
    return valid_moves


def get_board_with_valid_moves(board, tile, display_score=None):
    """
    Returns a new board with . marking the valid moves the given player can make.
    """
    dupe_board = get_board_copy(board)
    if display_score:
        for x, y in get_valid_moves(dupe_board, tile):
            temp_board = get_board_copy(board)
            make_move(temp_board, tile, x, y)
            score = get_score_of_board(temp_board)
            dupe_board[x][y] = score[tile]
    else:
        for x, y in get_valid_moves(dupe_board, tile):
            dupe_board[x][y] = '.'
    return dupe_board


def get_score_of_board(board):
    """
    Determine the score by counting the tiles. Returns a dictionary with keys
    'X' and 'O'.
    """
    xscore = 0
    oscore = 0
    for x in range(8):
        for y in range(8):
            if board[x][y] == 'X':
                xscore += 1
            if board[x][y] == 'O':
                oscore += 1
    return {'X': xscore, 'O': oscore}


def enter_player_tile():
    """
    Lets the player type which tile thay want to be.
    return a list with the player's tile as the first item, and the computer's
    tile as the second
    """
    tile = ''
    while not tile == 'X' or tile == 'O':
        print('Do you want to be "X" or "O"?')
        tile = input().upper()
    
    if tile == 'X':
        return ['X', 'O']
    else:
        return ['O', 'X']
    

def who_goes_first():
    """
    Randomly choose the player who goes first.
    """
    if random.randint(0, 1):
        return 'player'
    else:
        return 'computer'
    

def play_again():
    """
    return True if the player wants to play again.
    """
    print('Do you want to play again? (yes or no)')
    return input().lower().startswith('y')


def make_move(board, tile, xstart, ystart):
    """
    Place the tile on the board at xstart, ystart, and flip any of the opponent's
    pieces. Return False if this is an invalid move, True if it is valid.
    """
    tiles_to_flip = is_valid_move(board, tile, xstart, ystart)
    if not tiles_to_flip:
        return False
    
    board[xstart][ystart] = tile
    for x, y in tiles_to_flip:
        board[x][y] = tile
    return True


def is_on_corner(x, y):
    """
    Returns True if the position is in one of the four corners.
    """
    return [x, y] in [[0, 0], [7, 0], [0, 7], [7, 7]]


def get_player_move(board, player_tile):
    """
    Let the player type in their move.
    Returns the move as [x, y] (or returns the strings 'hints' or 'quit' 
    or 'super-hints'.)
    """
    DIGITS_1TO8 = '1 2 3 4 5 6 7 8'.split()
    while True:
        print('Enter your move, or type "quit" to end the game, or'
              ' "hints" to turn on/off hints.')
        print('If you think it is difficult for you to beat computer, try'
              ' to type "super-hints", and will be very helpful!')
        move = input().lower()
        if move == 'quit':
            return 'quit'
        elif move == 'hints':
            return 'hints'
        elif move == 'super-hints':
            return 'super-hints'
        
        if len(move) == 2 and move[0] in DIGITS_1TO8 and move[1] in DIGITS_1TO8:
            x = int(move[0]) - 1
            y = int(move[1]) - 1
            if is_valid_move(board, player_tile, x, y):
                break
            else:
                continue
        else:
            print('That is not a valid move. Type the x digit (1-8), then the y digit (1-8).')
            print('For example, 81 will be the top-right corner.')
    
    return [x, y]


def get_computer_move(board, computer_tile):
    """
    Given a board and the computer's tile, determine where to move and return that move as
    [x, y] list.
    """
    possible_moves = get_valid_moves(board, computer_tile)
    
    # Randomize the order of the possible moves.
    random.shuffle(possible_moves)
    
    for x, y in possible_moves:
        if is_on_corner(x, y):
            return [x, y]
    
    # Go through all the possible moves and remember the best scoring move.
    best_score = -1
    for x, y in possible_moves:
        dupe_board = get_board_copy(board)
        make_move(dupe_board, computer_tile, x, y)
        score = get_score_of_board(dupe_board)[computer_tile]
        if score > best_score:
            best_move = [x, y]
            best_score = score
    return best_move


def show_points(player_tile, computer_tile):
    """Print out the current score."""
    scores = get_score_of_board(main_board)
    print('You have %s points. The computer has %s points.'
          % (scores[player_tile], scores[computer_tile]))
    


# Use different color to show different tile.
if use_color:
    colorama.init(autoreset=True)
print('Welcome to Reversi!')

while True:
    # Reset the board and game.
    main_board = get_new_board()
    reset_board(main_board)
    player_tile, computer_tile = enter_player_tile()
    show_hints = False
    show_super_hints = False
    turn = who_goes_first()
    print('The {0} will go first.\n'.format(turn))
    
    while True:
        if turn == 'player':
            # Player's turn.
            if show_hints:
                valid_moves_board = get_board_with_valid_moves(main_board, player_tile)
                draw_board(valid_moves_board)
            elif show_super_hints:
                valid_moves_with_scores_board = get_board_with_valid_moves(
                    main_board, player_tile, display_score=True)
                draw_board(valid_moves_with_scores_board)
            else:
                draw_board(main_board)
            show_points(player_tile, computer_tile)
            move = get_player_move(main_board, player_tile)
            if move == 'quit':
                print('Thanks for playing!')
                sys.exit(0)
            elif move == 'hints':
                show_hints = not show_hints
                continue
            elif move == 'super-hints':
                show_super_hints = not show_super_hints
                continue
            else:
                make_move(main_board, player_tile, move[0], move[1])
                
            if get_valid_moves(main_board, computer_tile):
                turn = 'computer'
            else:
                break
        
        else:
            # Computer's turn.
            draw_board(main_board)
            show_points(player_tile, computer_tile)
            input('Press Enter to see the computer\'s move.\n')
            x, y = get_computer_move(main_board, computer_tile)
            make_move(main_board, computer_tile, x, y)
            
            if get_valid_moves(main_board, player_tile):
                turn = 'player'
            else:
                break
    
    # Display the final score.
    draw_board(main_board)
    scores = get_score_of_board(main_board)
    print('"X" scored {0} points. "O" scored {1} points.'.format(scores['X'], scores['O']))
    if scores[player_tile] > scores[computer_tile]:
        print('You beat the computer by {0} points! Congratulations!'.
              format(scores[player_tile]-scores[computer_tile]))
    elif scores[player_tile] < scores[computer_tile]:
        print('You lost. The computer beat you by {0} points.'.
              format(scores[computer_tile]-scores[player_tile]))
    else:
        print('The game was a tie!')
    
    if not play_again():
        break
