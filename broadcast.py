from socket import *
from random import randint
import threading 
import subprocess
import time
import copy

# first broadcast to check all neighbors 
def createSocket():
	# create a socket object
	s = socket(AF_INET, SOCK_DGRAM)
	s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
	return s

def broadcastInit(port):
	s = createSocket()
	data = b"Init"	
	# Broadcast this machine's IP
	s.sendto(data, ('<broadcast>', port))
		
	return s	

def broadcastClose(s):
	s.close()


def execute(function1, args1, function2, args2):
	# starting broadcast receriver
	thread1 = threading.Thread(target = function1, args = args1)
	thread1.daemon = True
	thread1.start()
	time.sleep(2)
	# getting neighbor membership list
	s=broadcastInit(port=9999)
	broadcastClose(s)
	time.sleep(5)
	
	thread2 = threading.Thread(target = function2, args = args2)
	thread2.daemon = True
	thread2.start()
	thread2.join()
	time.sleep(2)

