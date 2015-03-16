import os.path
class PathError(Exception):
	def __call__(self, *args):
		return self.__class__(*(self.args + args))
	def __str__(self):
		return ": ".join(self.args)

class VFS(object):
	def __init__(self, root):
		self.root = root

	def localize(func):
		def wrapper(self, *args):
			path = args[0]
			if path.find("..") != -1: # No haxoring your way out of the fs :P
				path = self.root
			if len(path) > 0:
				if path[0] == "/": # Ensure that nobody can access root
					if len(path) > 1:
						path = os.path.join(self.root, path[1:])
					else:
						path = self.root
			if path[:2] != self.root: # Ensure we don't inadvertantly double up our root dir string XD
				path = os.path.join(self.root, path) # Ensure no matter what we are operating out of the virtual directory
			path = os.path.normpath(path)        # Ensure our path is at least clean
			if len(args) > 1:
				return func(self, path, args[1])
			else:
				return func(self, path)
		return wrapper

	@localize
	def pathExist(self, path):
		print(path)
		if os.path.exists(os.path.abspath(path)):
			return True
		else:
			return False

	@localize
	def dirExist(self, path):
		if self.pathExist(path):
			if os.path.isdir(os.path.abspath(path)):
				return True
			else:
				return False
		else:
			return False

	@localize
	def fileExist(self, path):
		if self.pathExist(path):
			if os.path.isfile(os.path.abspath(path)):
				return True
			else:
				return False
		else:
			return False

	@localize
	def open(self, fname, method):
		if self.pathExist(os.path.dirname(fname)):
			return open(os.path.abspath(fname), method)

	@localize
	def walk(self, path):
		return os.walk(path)

	@localize
	def listdir(self, path):
		return os.listdir(path)

	def __str__(self):
		pass
		# TODO: Generate output similar to DOS tree command
