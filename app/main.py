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
	head = (body[0]['x'], body[0]['y'])
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
	print("Dont hit wall: ", moves)
	moves = dont_hit_enemies(moves, enemies, head)
	print("Dont hit snacc: ", moves)
	move = previous_head(moves, head, body)
	print('Go straight: ', move)

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

def dont_hit_enemies(moves, enemies, head):
	#checks side to side for enemy snakes
	if (head[0] +1, head[1]) in enemies and 'right' in moves:
		moves.remove('right')
	if (head[0] -1, head[1]) in enemies and 'left' in moves:
		moves.remove('left')
	#checks up and down for enemy snakes
	print("ENEMIES: ", enemies)
	print("HEAD: ", head)
	if (head[0], head[1] +1) in enemies and 'down' in moves:
		moves.remove('down')
	if (head[0], head[1] -1) in enemies and 'up' in moves:
		moves.remove('up')
	return moves

def previous_head(moves, head, body):
	if (head[0] +1, head[1]) == body[1]:
		last_move = ['left']
	if (head[0] -1, head[1]) == body[1]:
		last_move = ['right']
	if (head[0], head[1] +1) == body[1]:
		last_move = ['up']
	if (head[0], head[1] -1) == body[1]:
		last_move = ['down']
	return last_move

def straight_preference(move, moves):
	if last_move in moves:
		return move



application = bottle.default_app()

if __name__ == '__main__':
	bottle.run(
		application,
		host=os.getenv('IP', '0.0.0.0'),
		port=os.getenv('PORT', '8080'),
		debug=os.getenv('DEBUG', True)
	)
