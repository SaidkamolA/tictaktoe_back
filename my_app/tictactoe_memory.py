import random
from typing import Optional

games = {}

def generate_game_id():
    while True:
        game_id = str(random.randint(100, 999))
        if game_id not in games:
            return game_id

def check_winner_with_line(board):
    # строки
    for i in range(3):
        if board[i][0] and board[i][0] == board[i][1] == board[i][2]:
            return board[i][0], [[i,0],[i,2]]
    # столбцы
    for i in range(3):
        if board[0][i] and board[0][i] == board[1][i] == board[2][i]:
            return board[0][i], [[0,i],[2,i]]
    # диагонали
    if board[0][0] and board[0][0] == board[1][1] == board[2][2]:
        return board[0][0], [[0,0],[2,2]]
    if board[0][2] and board[0][2] == board[1][1] == board[2][0]:
        return board[0][2], [[0,2],[2,0]]
    return None, None

def new_game(user_id):
    game_id = generate_game_id()
    board = [[None for _ in range(3)] for _ in range(3)]
    # Рандомно назначаем X или O первому игроку
    if random.choice([True, False]):
        player_X_id = user_id
        player_O_id = None
    else:
        player_X_id = None
        player_O_id = user_id
    games[game_id] = {
        'board': board,
        'current': 'X',
        'winner': None,
        'winner_line': None,
        'score_X': 0,
        'score_O': 0,
        'score_draw': 0,
        'ready_X': False,
        'ready_O': False,
        'connected_X': player_X_id is not None,
        'connected_O': player_O_id is not None,
        'player_X_id': player_X_id,
        'player_O_id': player_O_id
    }
    return game_id, board, 'X', None, None

def join_game(game_id, symbol, user_id):
    game = games.get(game_id)
    if not game:
        return None, 'Game not found'
    # Если обе роли не заняты, назначаем оставшуюся фигуру
    if game['player_X_id'] is None and game['player_O_id'] != user_id:
        game['player_X_id'] = user_id
        game['connected_X'] = True
    elif game['player_O_id'] is None and game['player_X_id'] != user_id:
        game['player_O_id'] = user_id
        game['connected_O'] = True
    # Если уже назначено, просто отмечаем подключение
    if game['player_X_id'] == user_id:
        game['connected_X'] = True
    if game['player_O_id'] == user_id:
        game['connected_O'] = True
    return game, None

def get_player_symbol(game, user_id):
    if game['player_X_id'] == user_id:
        return 'X'
    if game['player_O_id'] == user_id:
        return 'O'
    return None

def move(game_id, row, col, symbol):
    game = games.get(game_id)
    if not game:
        return None, 'Game not found'
    if not (game.get('connected_X') and game.get('connected_O')):
        return None, 'Both players must be connected'
    if game['winner']:
        return None, 'Game is already finished'
    if symbol != game['current']:
        return None, 'Not your turn'
    if not (0 <= row < 3 and 0 <= col < 3):
        return None, 'Invalid cell'
    if game['board'][row][col] is not None:
        return None, 'Cell already taken'
    game['board'][row][col] = symbol
    winner, winner_line = check_winner_with_line(game['board'])
    if winner:
        game['winner'] = winner
        game['winner_line'] = winner_line
        if winner == 'X':
            game['score_X'] += 1
        elif winner == 'O':
            game['score_O'] += 1
    elif all(cell is not None for r in game['board'] for cell in r):
        game['winner'] = 'draw'
        game['winner_line'] = None
        game['score_draw'] += 1
    else:
        game['current'] = 'O' if symbol == 'X' else 'X'
    return game, None

def get_state(game_id):
    return games.get(game_id)

def ready_for_new_game(game_id, symbol):
    game = games.get(game_id)
    if not game:
        return None, 'Game not found'
    if symbol == 'X':
        game['ready_X'] = True
    elif symbol == 'O':
        game['ready_O'] = True
    if game['ready_X'] and game['ready_O']:
        game['board'] = [[None for _ in range(3)] for _ in range(3)]
        game['winner'] = None
        game['winner_line'] = None
        game['current'] = 'X'
        game['ready_X'] = False
        game['ready_O'] = False
    return game, None

def check_winner(board):
    winner, _ = check_winner_with_line(board)
    return winner 