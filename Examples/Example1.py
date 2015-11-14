from sqassistant import *
import random

class NetworkManager(Section):
	def __init__(self):
		Section.__init__(self, {"host":"localhost", "port":8000})

	def start(self, data):
		print("Starting Network, connecting to {host}:{port}".format(**data))
		return random.random() < 0.5    #Might work, might not

	def quit(self):
		print("Stopping Network, disconnecting")
		#returns None => Assistant uses default data

class DbManager(Section):
	def __init__(self):
		Section.__init__(self, {"path":"example.db"})

	def start(self, data):
		print("Starting Database, opening {path}".format(**data))
		return random.random() < 0.5    #Might work, might not

	def quit(self):
		print("Closing Database")
		return {"path":"newPath.db"}

class MainWindow(Section):
	def __init__(self):
		Section.__init__(self, {"geometry":(123, 456, 640, 480)})

	def start(self, data):
		print("Starting MainWindow, at {geometry}".format(**data))
		return random.random() < 0.5    #Might work, might not

	def quit(self):
		print("Stopping Network, disconnecting")
		#returns None => Assistant uses default data

if __name__ == '__main__':
	assist=Assistant([
		NetworkManager(),
		DbManager()
	], "LastSession.session", autoRollback=False)

	if not assist.start():
		print("- Start failed, doing rollback now")
		assist.rollback()
	else:
		print("- Successfully started")
		input("Press [Return] to quit")
		assist.quit()
