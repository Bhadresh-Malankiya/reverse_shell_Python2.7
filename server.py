#!/usr/bin/python

import socket
import json

def big_send(data):
	json_data = json.dumps(data)
	target.send(json_data)

def big_recv():
	json_data = ""
	while True:
		try:
			json_data = json_data + target.recv(1024)
			return json.loads(json_data)
		except ValueError:
			continue

#creating socket and setting up options 
def server():
	global ip
	global target
	global s
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
	
	s.bind(("127.0.0.1",44443))
	s.listen(5)


	target, ip = s.accept()
	print("Connected!! message from server")

def shell():
	while True:
		cmd = raw_input("SHELL~#$ %s" % str(ip))
		big_send(cmd)	
		if cmd == "q":
			print("Terminating connection from server.....")
			break
		else :
			result = big_recv()
			print(result)

server()
shell()
s.close()
