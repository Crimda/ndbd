from wst.fio import cfg
init = "*W*l:*m*0"
norm = "*W[*C*l*W] *m*0"
erro = "*W[*C*l*W] *R*m*0"
warn = "*W[*C*l*W] *Y*m*0"
good = "*W[*C*l*W] *G*m*0"

conf = cfg.Cfg()
conf.open("cfg/ndbd.cfg")

DEBUG = conf.get("debug")
DAT_DIR = conf.get("database")

HOST = conf.get("host")

try:
	PORT = int(conf.get("port"))
except:
	from wst.trm import log
	log.LOGGER = "NDBD->Config"
	log.FORMAT = "*R*l:*m*0"
	log.out("Unable to read port from config, defaulting to 65535")
	PORT = 65535

MAX_CLIENTS = conf.get("maxClients")
