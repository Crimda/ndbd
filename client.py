from wst.trm import log
from wst.utl import async

import sys
import socket
import time
NAME = "Wazubaba"
class Client(async.asyncore):

	def post(self, path, msg):
		fmsg = "%s - %s\n\
%s\n\n\
==========================================================\n" %(NAME, time.strftime("%d %b, %a %H:%M:%S"), msg)
		print(fmsg)
		sock.send("put %s %s" %(path, fmsg))

	def get(self, path):
		sock.send("get %s" %(path))

	def ls (self, path="/"):
		sock.send("ls %s" %(path))

	def process(self, interface):
		if interface == sys.stdin:
			cmd = interface.readline().strip("\r\n")
			try: path = cmd.split()[1]
			except: path = "NONE"
			try: data = cmd.split(" ",2)[2]
			except: data = "NONE"
			try: cmd = cmd.split()[0]
			except: pass

			print("DEBUG:\n\tcmd=%s\n\tpth=%s\n\tdat=%s\n"%(cmd, path, data))

			if cmd in ["s", "send", "put", "push", "p"]:
				if data != "NONE" and path != "NONE":
					self.post(path, data)
				else:
					print("Error: Missing parameters.\n\tUSAGE: [s,send,put,push,p] path message")

			elif cmd in ["g", "get", "pull"]:
				if path != "NONE":
					self.get(path)
				else:
					print("Error: Missing parameters.\n\tUSAGE: [g,get,pull] path")

			elif cmd in ["q", "sd", "shutdown", "quit", "k", "kill"]:
				self.running = False
				sock.close()
				time.sleep(1)

			elif cmd in ["ls"]:
				if path != "NONE":
					self.ls(path)
				else:
					print("Error: Missing parameters.\n\tUSAGE: [ls] path")

		elif interface == sock:
			data = sock.recv(512)
			if data == "": self.running = False
			else:
				sys.stdout.write(data)

sock = socket.socket()
sock.connect(("localhost", 65535))

client = Client({
	"readers": [sys.stdin, sock],
	"writers": [],
	"excepts": [],
})

client.start()
