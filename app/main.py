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
    return "<h1>Hello World</h1>"

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
    print('(Wall) Safe Moves: ', moves)

    moves = dont_hit_enemies(moves, enemies, head)
    print('(Enemies) Safe Moves: ', moves)

    moves = dont_get_cornered(moves, enemies, head)
    print('(Cornered) Safe Moves: ', moves)

    moves = away_from_walls(moves, height, width, head)
    print('(Wall Away) Good Directions: ', moves)

    # Restricting
    ################################################
    # Choosing

    move = eat_close_food(moves, head, food)
    print('Eat food! ', move)

    if not move:
        move = previous_head(moves, head, body)
        print('Go straight: ', move)

    if not move:
        move = random.choice(moves)

    print('Preferred moves: ', move)

    return {
        'move': move
    }

#function avoids walls
def dont_hit_wall(moves, height, width, head):
    if head[0] == width -1 and 'right' in moves:
        moves.remove('right')
    elif head[0] == 0 and 'left' in moves:
        moves.remove('left')
    if head[1] == height -1 and 'down' in moves:
        moves.remove('down')
    elif head[1] == 0 and 'up' in moves:
        moves.remove('up')
    return moves

#function avoids enemy coordinates
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

#function avoids situations where it would be cornered even if the space is open
def dont_get_cornered(moves, enemies, head):
    if (head[0] +1, head[1] -1) and (head[0] +1, head[1] +1) and (head[0] +2, head[1]) in enemies and 'right' in moves:
        moves.remove('right')
    if (head[0] -1, head[1] -1) and (head[0] -1, head[1] +1) and (head[0] -2, head[1]) in enemies and 'left' in moves:
        moves.remove('left')
    if (head[0] +1, head[1] +1) and (head[0] -1, head[1] +1) and (head[0], head[1] +2) in enemies and 'down' in moves:
        moves.remove('down')
    if (head[0] +1, head[1] -1) and (head[0] -1, head[1] -1) and (head[0], head[1] -2) in enemies and 'up' in moves:
        moves.remove('up')
    return moves

#move away from walls in open ended situations
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

#if food is in adjacent cells eat it
def eat_close_food(moves, head, food):
    if (head[0] +1, head[1]) in food and 'right' in moves:
        return 'right'
    if (head[0] -1, head[1]) in food and 'left' in moves:
        return 'left'
    if (head[0], head[1] +1) in food and 'down' in moves:
        return 'down'
    if (head[0], head[1] -1) in food and 'up' in moves:
        return 'up'

#gets the previous move
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

#prefers straight play in open-ended situations
def straight_preference(move, moves):
    if move in moves:
        return [move]
    else:
        return moves

application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug=os.getenv('DEBUG', True)
    )
