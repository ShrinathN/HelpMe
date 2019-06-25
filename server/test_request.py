#!/bin/python
#this script will throw randomly generated requests
import random
import time
import socket
import json

def rand_string(num):
	to_return = ''
	character_map = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
	for i in range(num):
		to_return = to_return + str(character_map[random.randint(0, len(character_map) - 1)])
	return to_return

def rand_bool():
	return bool(round(random.random()))

#macros
ADDRESS = ("127.0.0.1",8080)

while(True):
	connector_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
	connector_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR | socket.SO_REUSEPORT, 1)
	data_to_send = {
	"user_location" : str(random.random()) + ' ' + str(random.random()),
	"user_name" : str(rand_string(random.randint(10,20))),
	"user_mobile" : random.randint(1000000000,9999999999),
	"user_need_food" : rand_bool(),
	"user_need_water" : rand_bool(),
	"user_need_healthcare" : rand_bool(),
	"user_text" : str(rand_string(random.randint(100,250))),
	"user_urgency_level" : random.randint(1,4)
	}
	connector_socket.connect(ADDRESS)
	print(data_to_send)
	connector_socket.send(bytes(str.encode(json.dumps(data_to_send), 'utf-8')))
	connector_socket.close()
	time.sleep(0.1)