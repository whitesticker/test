from socket import *
from random import randint
from broadcast import *
import threading 
import subprocess
import time
import copy

memlistYK = dict()
memlistZK = dict()
roundlistYK = dict()
roundlistZK = dict()


lock_k = threading.Lock()

# reply to broadcast
def broadcastReceive(port):
	global memlistYK
	global memlistZK
	global roundlistYK
	global roundlistZK
	serversocket = createSocket()
	'''
	output = subprocess.Popen('ifconfig | grep "inet addr:192" | cut -d ":" -f 2 |  cut -d " " -f 1',
				  shell = True, stdout = subprocess.PIPE, )
	#get hostname and port
	host = output.communicate()[0].strip()
	'''
	#bind to broadcast port
	serversocket.bind(('<broadcast>', port))

	while True:	
		msg = serversocket.recvfrom(1024)
		client = msg[1][0]
		clientPort = msg[1][1]
		if msg[0] == b'Init':
			memlistZK.update({client: 0 }  )
			memlistYK.update({client: 0 } )
			roundlistZK.update({client: 0 }  )
			roundlistYK.update({client: 0 }  )
			# print(roundlistYK)
		elif b'Yk' in msg[0] or b'Zk' in msg[0]:
			lock_k.acquire()			
			# print(roundlistYK)
			round_num = msg[0].decode("utf-8") .split(',')[0].split(':')[1].strip()
			yk_value = msg[0].decode("utf-8") .split(',')[1].split(':')[1].strip()
			zk_value = msg[0].decode("utf-8") .split(',')[2].split(':')[1].strip()
			if int(round_num) > int(roundlistYK[client]):
				roundlistYK[client] = round_num
				memlistYK[client] = float(yk_value)
				roundlistZK[client] = round_num		
				memlistZK[client] = float(zk_value)
			lock_k.release()
		else:
			pass
		print("Got a connection from %s, %s with msg: %s" % (msg[1][0], msg[1][1], msg[0]))	

def broadcastSend(numberY, numberZ, port):
	'''	
	output = subprocess.Popen('ifconfig | grep "inet addr:192" | cut -d ":" -f 2 |  cut -d " " -f 1',
				  shell = True, stdout = subprocess.PIPE, )
	host = output.communicate()[0].strip()
	'''	
	# create a socket object
	s = createSocket()
	
	yk = numberY
	zk = numberZ
	sendTotalY = 0
	prevSumY = 0	
	sendTotalZ = 0
	prevSumZ = 0	
	
	for rnd in range(1, 20): 		
		time.sleep(2.0)	
		sendTotalY += float(yk)/len(memlistYK)
		sendTotalZ += float(zk)/len(memlistZK)
		data = b"Round:%d, Yk:%f, Zk:%f" % (rnd, sendTotalY, sendTotalZ)
		s.sendto(data, ('<broadcast>', port))
	
		time.sleep(2.0)
		temp_sum = 0
		lock_k.acquire()						
		for client in memlistYK:
			if rnd <= int(roundlistYK[client]):
				temp_sum += memlistYK[client]
		yk = temp_sum - prevSumY
		prevSumY = temp_sum
		temp_sum = 0
		for client in memlistZK:
			if rnd <= int(roundlistZK[client]):
				temp_sum += memlistZK[client]
		zk = temp_sum - prevSumZ
		prevSumZ = temp_sum
		lock_k.release()
	# close socket in the end
	broadcastClose(s)

if __name__ == "__main__":
	execute( broadcastReceive, (9999,), broadcastSend, (6,1,9999) )






