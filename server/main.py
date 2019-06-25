#!/bin/python
import socket
import json
import pandas
import os

#for in-app database
in_app_database = {
'user_location' : [],
'user_name' : [],
'user_mobile' : [],
'user_need_food' : [],
'user_need_water' : [],
'user_need_healthcare' : [],
'user_text' : [],
'user_urgency_level' : []
}

#creating database, or using pre-existing database
try:
	os.listdir('db.csv')
except NotADirectoryError: #in case the database already exists
	data_frame = pandas.DataFrame(in_app_database)
	data_frame.to_csv('db.csv') #saving shit to file
except FileNotFoundError: #this means the database does not already exist
	

#creating socket to listen etc
listener_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
listener_socket.bind(("127.0.0.1",8080))
listener_socket.listen(10)

while(True):
	acceptor_socket, address_client = listener_socket.accept()
	recvd_data = acceptor_socket.read(10240)
	recvd_report = json.loads(recvd_data)
	