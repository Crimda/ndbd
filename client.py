from wst.trm import log
from wst.utl import async

import sys
import socket
import time

class Client(async.asyncore):
	def process(self, interface):
		if interface == sys.stdin:
			cmd = interface.readline().strip("\r\n")
			if cmd in ["q", "sd", "shutdown"]:
				self.running = False
				sock.close()
				time.sleep(1)
			else:
				sock.send(cmd)

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
