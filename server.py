from wst.trm import log
from wst.utl import async

import socket
import os
import sys
import time

from shared import *
import fileio

log.LOGGER = "NDBD"
log.FORMAT = init

if DEBUG:
	log.out("Enabled StackTrace Debugging")
	import traceback

class Server(async.asyncore):

	def say(self, client, msg):
		try:
			client.send(msg+'\n')
		except socket.error:
			log.FORMAT = erro
			log.out("Unable to send message, client inaccesable")

	def kick(self, client, msg = ""):
		log.FORMAT = warn
		log.out(msg)
		self.say(client, "connection terminated")

		client.close()

		self.monitors["readers"].remove(client)
		self.updateCNum()

	def updateCNum(self):
		#Note: I seriously just made this because it's easier to type than
		#its definition :P
		self.numClients = len(self.monitors["readers"]) - 2

	def handler(self, data, client):
		data = data.strip("\r\n")
		log.FORMAT = good
		log.out("Data from %s:%s recieved" %(client.getsockname()))
		log.FORMAT = init
		log.out(data)
		if " " in data:
			if len(data.split()) > 2:
				cmd, path, data = data.split(" ", 2)
			elif len(data.split()) == 2:
				cmd, path, = data.split(" ", 1)
				data = ""
			elif len(data.split()) == 1:
				cmd = data
				path = ""
				data = ""
		else:
			cmd = ""
			path = ""
			data = ""

		log.FORMAT = warn
		log.out("cmd=%s\npath=%s\ndata=%s" %(cmd, path, data))

		if cmd == "get":
			if path == None:
				self.invalidReq(client)
			else:
				self.serve(path, client)
		elif cmd == "put":
			if path == None:
				self.invalidReq(client, "Missing path!")
			elif data == None:
				self.invalidReq(client, "Missing data!")
			else:
				self.take(path, data, client) # Include client for post IP logging
		elif cmd == "ls":
			if path == None:
				self.invalidReq(client)
			else:
				self.listDirs(path, client)
		else:
			self.invalidReq(client, "Unknown data")

	def listDirs(self, path, client):
		log.FORMAT = norm
		ip, port = client.getsockname()
		log.out("Client %s:%s has requested ls of dir %s" %(ip, port, path))

		data = fileio.ls(path)
		if data == -1:
			self.kick(client, "Client %s:%s has attempted to use \"..\". May be attempting to access root filesystem!"%(ip, port))
		elif data == False:
			client.send("ERR Path does not exist\n")
		else:
			client.send(str(len(data[0]))+'\n') # send number of dirs
			for hit in data[0]:
				client.send(hit+'\n')
			client.send(str(len(data[1]))+'\n') # send number of files
			for hit in data[1]:
				client.send(hit+'\n')


	def serve(self, path, client):
		log.FORMAT = norm
		ip, port = client.getsockname() # Because this returns a fking tuple...
		log.out("Client %s:%s has requested %s" %(ip, port, path))
		data = fileio.get(path)
		log.FORMAT = warn
		log.out(data)
		if data == -1:
			self.kick(client, "Client %s:%s has attempted to use \"..\". May be attempting to access root filesystem!"%(ip, port))
		elif data == False:
			client.send("ERR File does not exist\n")
		else:
			client.send(data)


	def take(self, path, data, client):
		log.FORMAT = norm
		ip, port = client.getsockname()
		log.out("Client %s:%s has pushed data [%s] to path: %s" %(ip, port, data, path))
		data = fileio.set(path, data)
		if data == -1:
			self.kick(client, "Client %s:%s has attempted to use \"..\". May be attempting to access root filesystem!"%(ip, port))
		elif data == False:
			client.send("ERR Unable to create file\n")
		elif data == True:
			client.send("Post successful\n")

	def invalidReq(self, client, reason=""):
		ip, port = client.getsockname()
		log.FORMAT = warn
		if reason != "":
			log.out("Invalid request from %s:%s: %s" %(ip, port, reason))
		else:
			log.out("Invalid request from %s:%s" %(ip, port))
		self.say(client, "ERR Invalid Req\n")
		client.close()
		self.monitors["readers"].remove(client)
		self.updateCNum()

	def cmdHandler(self, cmd):
		if cmd in ["q","sd", "kill", "shutdown"]:
			log.FORMAT = warn
			log.out("Shutting down...")

			for client in self.monitors["readers"]:
				if client != sys.stdin and client != sock:
					client.send("Server Shutdown")
					self.kick(client, "Terminating connection to %s:%s due to server shutdown" %(client.getsockname()))

			self.running = False
			sock.close()
			time.sleep(1)

	def process(self, interface):
		if interface == sys.stdin:
			cmd = interface.readline().strip("\r\n")
			self.cmdHandler(cmd)

		elif interface == sock:
			if self.acceptClients:
				if len(self.monitors["readers"]) - 2 <= self.maxClients:
					client, address = sock.accept()
					log.FORMAT = norm
					log.out("Connection from %s:%s established" %(client.getsockname()))

					client.settimeout(5.0)

					self.monitors["readers"].append(client)
					self.updateCNum()
				else:
					log.FORMAT = warn
					log.out("Max clients reached, dropping connection!")

					client.close()

		else:
			try:
				data = interface.recv(256)
				if data:
					self.handler(str(data), interface)
				else:
					self.kick(interface, msg = "Connection from %s:%s closed by remote" %(interface.getsockname()))
			except Exception as e:
				self.kick(interface, msg = "Connection from %s:%s removed due to protocol mismatch" %(interface.getsockname()))
				log.FORMAT = warn
				log.out("Error: %s" %(e))
				log.out("Stacktrace:\n%s" %(traceback.format_exc()))

log.out("Initializing...")

sock = socket.socket()

server = Server({
	"readers": [sys.stdin, sock],
	"writers": [],
	"excepts": [],
})

server.acceptClients = True
server.maxClients    = MAX_CLIENTS

log.out("Binding socket...")

try:
	sock.bind((HOST, PORT))
	sock.listen(5)
except socket.error as e:
	log.FORMAT = erro
	log.out("Unable to bind port, Address already in use!")
	log.FORMAT = init
	log.out("Stacktrace:\n%s" %(traceback.format_exc()))
	sys.exit()

log.FORMAT = good
log.out("Reactor started...")
log.FORMAT = norm
server.start()

log.FORMAT = good
log.out("Server shutdown successfully.")
