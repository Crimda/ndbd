#import fileio
#fileio.ls("/p/python")
#fileio.ls("/p/python/../")
#fileio.set("/p/python/hammers", "Wazubaba - 14 Mar, Sat 23:20:55\nThis is some test data \o/\n\n==========================================================\n")
#print(fileio.get("/p/python/hammers"))
#fileio.update()
#fileio.test()
import vfs
fs = vfs.VFS("db")
#fs.global2local("p")
#fs.chdir("p")

test = fs.open("testfile", "r")
if not test:
	print("Error opening testfile!")
	print("Got type: %s" %(type(test)))
else:
	print(test.read())
	test.close()

meow = fs.open("p/vfsTestFile", "a")
if not meow:
	print("Error opening p/vfsTestFile!")
else:
	meow.write("HammerDogs!\n")
	meow.close()

meow = fs.open("p/vfsTestFile", "r")
if not meow:
	print("Error re-opening p/vfsTestFile!")
else:
	print(meow.read())
	meow.close()

#for path, dirs, files in fs.walk("/../../"):
#	print path, dirs, files

print(fs.listdir(""))
