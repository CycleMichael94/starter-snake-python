import json
import os
import random
import bottle

LEFT = 'left'
RIGHT = 'right'
UP = 'up'
DOWN = 'down'

@bottle.route('/')
def index():
    return "<h1>I'm a weenie</h1>"

@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')

@bottle.post('/ping')
def ping():
    return {}

@bottle.post('/start')
def start():
    return {
        "color": '#444444',
        "taunt": "Sup bod?"
    }

@bottle.post('/end')
def end():
    return {}




@bottle.post('/move')
def move():
    data = bottle.request.json

    you = data['you']
    health = you['health']
    body = [ (b['x'], b['y']) for b in you['body'] ]
    length = len(body)
    head = (body[0])
    board = data['board']
    height = board['height']
    width = board['width']
    snakes = board['snakes']
    food = [ (f['x'], f['y']) for f in board['food'] ]
    enemies = []
    tail = []
    moves = ['left', 'right', 'up', 'down']

    for snake in snakes:
        enemy_location = snake['body']
        for e in enemy_location:
            enemies.append((e['x'],e['y']))

    moves = dont_hit_wall(moves, height, width, head)
    print('Dont hit wall: ', moves)
    moves = dont_hit_enemies(moves, enemies, head)
    print('Dont hit snacc: ', moves)
    move = previous_head(moves, head, body)
    print('Go straight: ', move)
    move = away_from_walls(moves, height, width, head)
    print('Go away from walls: ', move)
    move = eat_close_food(moves, head, food)
    print('Eat food! ')
    move = dont_get_cornered(moves, head)
    print('Dont get cornered: ', moves)

    if move not in moves:
        move = random.choice(moves)

    return {
        'move': move
    }

def dont_hit_wall(moves, height, width, head):
    #side walls avoidance
    if head[0] == width -1 and 'right' in moves:
        moves.remove('right')
    elif head[0] == 0 and 'left' in moves:
        moves.remove('left')
    #ceiling and floor avoidance
    if head[1] == height -1 and 'down' in moves:
        moves.remove('down')
    elif head[1] == 0 and 'up' in moves:
        moves.remove('up')
    return moves

def dont_hit_enemies(moves, enemies, head):
    if (head[0] +1, head[1]) in enemies and 'right' in moves:
        moves.remove('right')
    if (head[0] -1, head[1]) in enemies and 'left' in moves:
        moves.remove('left')
    if (head[0], head[1] +1) in enemies and 'down' in moves:
        moves.remove('down')
    if (head[0], head[1] -1) in enemies and 'up' in moves:
        moves.remove('up')
    return moves

def dont_get_cornered(moves, head):
    if (head[0] +1, head[1] -1) and (head[0] +1, head[1] +1) and (head[0] +2, head[1]) in enemies and 'right' in moves:
        moves.remove('right')
    if (head[0] -1, head[1] -1) and (head[0] -1, head[1] +1) and (head[0] -2, head[1]) in enemies and 'right' in moves:
        moves.remove('left')
    if (head[0] +1, head[1] +1) and (head[0] -1, head[1] +1) and (head[0], head[1] +2) in enemies and 'right' in moves:
        moves.remove('down')
    if (head[0] +1, head[1] -1) and (head[0] -1, head[1] -1) and (head[0], head[1] -2) in enemies and 'right' in moves:
        moves.remove('up')

def previous_head(moves, head, body):
    last_move = None
    if (head[0] +1, head[1]) == body[1]:
        last_move = 'left'
    if (head[0] -1, head[1]) == body[1]:
        last_move = 'right'
    if (head[0], head[1] +1) == body[1]:
        last_move = 'up'
    if (head[0], head[1] -1) == body[1]:
        last_move = 'down'
    return last_move

def straight_preference(move, moves):
    if move in moves:
        return [move]
    else:
        return moves

def eat_close_food(moves, head, food):
    if (head[0] +1, head[1]) in food and 'right' in moves:
        return 'right'
    if (head[0] -1, head[1]) in food and 'left' in moves:
        return 'left'
    if (head[0], head[1] +1) in food and 'down' in moves:
        return 'down'
    if (head[0], head[1] -1) in food and 'up' in moves:
        return 'up'

def away_from_walls(moves, height, width, head):
    if len(moves) <= 2:
        return moves
    if head[0] > width -3 and 'right' in moves:
        moves.remove('right')
    if head[0] < width +3 and 'left' in moves:
        moves.remove('left')
    if head[1] > height -3 and 'down' in moves:
        moves.remove('down')
    if head[1] < height +3 and 'up' in moves:
        moves.remove('up')
    return moves


application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug=os.getenv('DEBUG', True)
    )
