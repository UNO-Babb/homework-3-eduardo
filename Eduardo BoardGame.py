from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# Define the game board and units
board_size = 15
unit_types = {
    'Infantry': {'health': 4, 'damage': 1, 'icon': 'unit-Infantry'},
    'Heavy Infantry': {'health': 6, 'damage': 2, 'icon': 'unit-Heavy-Infantry'},
    'Armor Car': {'health': 8, 'damage': 7, 'icon': 'unit-Armor-Car'},
    'Armor Mech': {'health': 10, 'damage': 9, 'icon': 'unit-Armor-Mech'}
}

# Player nations and colors
nations = {
    'Rebel Forces': 'blue',
    'Naxos': 'green',
    'Ninja Nation': 'red',
    'Cyborg Army': 'brown'
}

players = {}

@app.route('/')
def index():
    return render_template('board.html', board_size=board_size, nations=nations)

@app.route('/create_game', methods=['POST'])
def create_game():
    data = request.json
    player_count = data['player_count']
    player_info = data['player_info']  # List of player selections (nation and flag location)
    
    game_data = {
        'players': {},
        'board': [[None for _ in range(board_size)] for _ in range(board_size)],
        'turn': 0
    }

    # Set up each player's nation and flag
    for i, player in enumerate(player_info):
        game_data['players'][f'Player{i+1}'] = {
            'nation': player['nation'],
            'flag': player['flag'],
            'units': [],
            'color': nations[player['nation']],
            'turn': i == 0
        }

    players[game_data['turn']] = game_data
    return jsonify(game_data)

@app.route('/place_unit', methods=['POST'])
def place_unit():
    game_data = players.get(request.json['turn'])
    player = request.json['player']
    unit_type = request.json['unit_type']
    position = request.json['position']

    # Place the unit
    unit_id = random.randint(1000, 9999)
    unit = {
        'id': unit_id,
        'type': unit_type,
        'health': unit_types[unit_type]['health'],
        'damage': unit_types[unit_type]['damage'],
        'position': position
    }
    game_data['players'][player]['units'].append(unit)
    
    # Place unit on board
    x, y = position
    game_data['board'][x][y] = unit
    return jsonify(game_data)

@app.route('/move_unit', methods=['POST'])
def move_unit():
    game_data = players.get(request.json['turn'])
    player = request.json['player']
    unit_id = request.json['unit_id']
    new_position = request.json['new_position']

    # Find and move unit
    for unit in game_data['players'][player]['units']:
        if unit['id'] == unit_id:
            unit['position'] = new_position
            break
    
    return jsonify(game_data)

if __name__ == '__main__':
    app.run(debug=True)
