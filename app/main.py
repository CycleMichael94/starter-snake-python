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
    body = you['body']
    length = len(body)
	head = body[0]
    board = data['board']
	height = board['height']
	width = board['width']
    snakes = board['snakes']
    food = board['food']
    enemies = []
	tail = []
	moves = ['left', 'right', 'up', 'down']

	for b in body:
		tail.append((b['x'],b['y']))

    for snake in snakes:
        enemy_location = snake['body']
		for e in enemy_location:
			enemies.append((e['x'],e['y']))

	moves = dont_hit_wall(moves, height, width, head)


	#enemy coordinates that match the three potential moves of my snake
    #own coordinates
	#the wall
        #pass

    #def okay_location:
    #enemy locations that are beside the three potential moves of my snakes
    #potential locations next to walls
        #pass

    #def good_location:
    #potential locations with no surrounding obstacles
    #food coordinates
        #pass

    #def find_food:
    #returns closest food coordinates and moves towards that
        #pass

    return {
        "move": random.choice(moves)
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



application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug=os.getenv('DEBUG', True)
    )
