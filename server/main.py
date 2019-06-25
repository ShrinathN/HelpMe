#!/bin/python
import socket
import json
import pandas
import os
import time

#macros
DB_FILE_NAME = 'db.csv'

#for in-app database
database_structure = {
'user_request_timestamp' : [],
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
	os.listdir(DB_FILE_NAME)
except NotADirectoryError: #in case the database file already exists
	data_frame = pandas.read_csv(DB_FILE_NAME)
except FileNotFoundError: #this means the database does not already exist
	data_frame = pandas.DataFrame(database_structure)
	data_frame.to_csv(DB_FILE_NAME) #saving the newly made dataframe to file

#creating socket to listen etc
listener_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
listener_socket.bind(("127.0.0.1", 8080))
listener_socket.listen(10)
print('[INFO]\tListening for connection...')

while(True):
	#getting data from the client
	acceptor_socket, address_client = listener_socket.accept() #acceptor socket accepting connection
	print('[INFO]\tConnection from ', address_client[0])
	recvd_data = acceptor_socket.read(10240) #reading data, data limit is 10KB
	recvd_report = json.loads(recvd_data) #parsing data to recvd_report
	acceptor_socket.close()
	
	#adding new data to data frame
	data_frame['user_request_timestamp'].append(time.ctime())
	data_frame['user_location'].append(recvd_report['user_location'])
	data_frame['user_name'].append(recvd_report['user_name'])
	data_frame['user_mobile'].append(recvd_report['user_mobile'])
	data_frame['user_need_food'].append(recvd_report['user_need_food'])
	data_frame['user_need_water'].append(recvd_report['user_need_water'])
	data_frame['user_need_healthcare'].append(recvd_report['user_need_healthcare'])
	data_frame['user_text'].append(recvd_report['user_text'])
	data_frame['user_urgency_level'].append(recvd_report['user_urgency_level'])

	#sorting data according to priority
	data_frame = data_frame.sort_values('user_urgency_level', ascending=False)
	
	data_frame.to_csv(DB_FILE_NAME)