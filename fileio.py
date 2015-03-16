import os
from wst.trm import log
from shared import *
#EXC = []
DB = "db/"
ERR = "|ERR|"

log.LOGGER = "NDBd->fileio"

def security(func):
	def wrap(*args, **kwargs):
#		print("yelhai")
		try:
			try: # this ugly thing basically lets us grab from either kwargs or args
				path = kwargs["path"]
			except:
				try:
					path = args[0]
				except IndexError:
					raise IndexError

		except IndexError:
			return func()

		if path.find("..") != -1: # ensure we can only accept full paths
			path = ERR
		if path[0] == '/': path = DB+path[1:]

		try:
			try:
				data = kwargs["data"]
			except:
				try:
					data = args[1]
				except IndexError:
					raise IndexError

#			print("calling with path and data")
			return func(path,data)
		except IndexError:
#			print("calling with only path")
			return func(path)
	return wrap

@security
def ls(path=DB):
	"""
		Synopsis: Return list of files and directories
		Takes: string path to directory
		Returns: tuple of two lists, one directories, one files,
		or -1 if odd attempt. False if path does not exist
	"""
	if path == ERR: return -1
#	if path[len(path)-1] != '/': path += '/' # This is the only function that will always take a dir path
	retval = ([],[])
	try:
		for entry in os.listdir(path):
			if os.path.isdir(path+entry):
				retval[0].append(entry)
			else:
				retval[1].append(entry)
	except OSError:
		return False

	return retval

@security
def get(path):
	"""
		Synopsis: Return content of a specific file
		Takes: string path to file
		Returns: string data of file or bool False if
		file does not exist, -1 if odd attempt
	"""
	if path == ERR: return -1
	try:
		fp = open(path, "r")
		fdat = fp.read()
		fp.close()
		return fdat
	except IOError:
		return False

@security
def set(path, data):
	"""
		Synopsis: Either create or append data to a file
		Takes: string path to file, string data to append
		Returns: bool success, or -1 if odd attempt
	"""
	if path == ERR: return -1

#	log.FORMAT = norm
#	log.out("%s\n^->%s" %(path, data))
#	log.FORMAT = init
	try:
		fp = open(path, "a")
		fp.write(data)
		fp.close()
		return True
	except IOError:
		return False
