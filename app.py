from flask import Flask, request, session
from tictactoe import TicTacToe, GameException
import os

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

games = []

@app.route('/start-game/<int:size>')
def start_game(size):
    if size < 3 or size > 10:
        return 'Choose a size from 3 to 10\n', 400
    game = TicTacToe(size)
    game_id = len(games)
    games.append({
        'game': game,
        'players': 1,
        'size': size,
    })
    session.setdefault('games', {})
    session['games'][game_id] = 'X'
    return (f'Welcome to HTTP TicTacToe\n'
            f'A little hack for MLH INIT 2021\n'
            f'Your game id is: {len(games) - 1}\n'), 200

@app.route('/list-open-games')
def list_games():
    open_games = [ f'{i}\t{game["size"]}' 
                   for i, game in enumerate(games) 
                   if game['players'] == 1 
                   and ('games' not in session or str(i) not in session['games']) ]
    if len(open_games) == 0:
        return 'No open games\n', 200
    return 'ID\tBoard Size\n' + '\n'.join(open_games) + '\n', 200

@app.route('/join-game/<int:game_id>')
def join_game(game_id):
    if game_id < 0 or game_id > len(games) - 1:
        return 'Invalid game ID\n', 400
    game = games[game_id]
    if game['players'] == 2:
        return 'Game is full\n', 200
    game['players'] += 1
    session.setdefault('games', {})
    session['games'][game_id] = 'O'
    return f'You joined game {game_id}\n', 200

@app.route('/get-games')
def get_games():
    return f'{session["games"]}'

@app.route('/who-am-i/<int:game_id>')
def who_am_i(game_id):
    if game_id < 0 or game_id > len(games) - 1:
        return 'Invalid game ID\n', 400
    if 'games' not in session or str(game_id) not in session['games']:
        return 'You are not in this game\n', 200
    return f'In game {game_id} you are player {session["games"][str(game_id)]}\n', 200

@app.route('/status/<int:game_id>')
def status(game_id):
    if game_id < 0 or game_id > len(games) - 1:
        return 'Invalid game ID\n', 400
    game = games[game_id]['game']
    return (f'Game {game_id} currently looks like this:\n'
            f'{str(game)}\n'
            f'Status: {game.next_player()}\n'), 200

@app.route('/play/<int:game_id>')
def play(game_id):
    if game_id < 0 or game_id > len(games) - 1:
        return 'Invalid game ID\n', 400
    game = games[game_id]['game']
    game_id = str(game_id)
    if 'games' not in session or game_id not in session['games']:
        return 'You are not part of this game.\n', 403
    x = request.args.get('row')
    y = request.args.get('col')
    if x is None or y is None:
        return 'Please specify position to play (row, col)\n', 400
    try:
        game.play(int(x), int(y), session['games'][game_id])
    except GameException as e:
        return f'{e}\n', 400
    if game.over:
        return 'You won!', 200
    return f'Success. Status: {game.next_player()}\n', 200
