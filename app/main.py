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
	return "<h1>I'm Nat and this is my snake</h1>"

@bottle.route('/static/<path:path>')
def static(path):
	return bottle.static_file(path, root='static/')

@bottle.post('/ping')
def ping():
	return {}

@bottle.post('/start')
def start():
	return {
		"color": '#AA22AA',
		"taunt": "My first program, go nice"
	}

@bottle.post('/end')
def end():
	return {}




@bottle.post('/move')
def move():
    data = bottle.request.json

    you = data.get('you')
    health = you['health']
    body = you['body']
    length = len(body)
    board = ['board']
    snakes = board['snakes']
    food = board['food']
    enemies = set()

    for snake in snakes:
        enemy_location = snake['body']
        enemies.append(enemy_location)

    for own_snake in body:
        pass

    #def bad_location:
    #enemy coordinates that match the three potential moves of my snake
    #own coordinates
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
		"move": move
	}



application = bottle.default_app()

if __name__ == '__main__':
	bottle.run(
		application,
		host=os.getenv('IP', '0.0.0.0'),
		port=os.getenv('PORT', '8080'),
		debug=os.getenv('DEBUG', True)
	)
