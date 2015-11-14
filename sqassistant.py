#!/usr/bin/python3
import pickle

class Section:
	"""
	Any section of your application should be subclassed by Section.
	e.g. a section for managing the network connections

	it should implement the start() and quit() methods
	"""
	def __init__(self, defaultData=None):
		"""
		Initializes the section
		"""
		self._started=False
		self._data=defaultData

	def start(self, data):
		"""
		Starts the section; is invoked by StartQuitAssistant
		Returns True if the section has been started successfully.
		Reimplement this method to e.g. connect the application to a server.
		:param data: bytes
		:return: bool
		"""
		return True

	def quit(self):
		"""
		Shuts down this section; is invoked by StartQuitAssistant
		Returns data to save in the sessionFile
		Reimplement this method to e.g. disconnect the application from a server.
		"""
		return None

class Assistant(object):
	"""
	Helps to start and quit applications
	"""
	def __init__(self, sections, sessionFile=None, autoRollback=True):
		"""
		:param sections: list of all sections
		:param sessionFile: path of the session file
		"""
		self.sections=sections
		self.sessionFile=sessionFile
		self.autoRollback=autoRollback

	def addSection(self, section):
		"""
		Adds a section to the assistant's section list.

		:param section: any object with a 'start' and 'quit' method
		"""
		self.sections.append(section)

	def start(self):
		"""
		Starts all sections.

		If a sessionFile is set, it loads the data before. If a section fails to start (i.e. returns False), a rollback is done if autoRollback is True.
		:return: True if everything was started successfully, else False
		"""
		self.loadSession()  #Put session data in section._data attributes
		for section in self.sections:
			successful=section.start(section._data) #Invoke section.start
			section._started=True
			if not successful:
				if self.autoRollback:
					self.rollback() #Quit all started sections
				return False
		return True

	def quit(self):
		"""
		Stops all sections.

		If a sessionFile is set, it stores the data returned by section.quit().
		"""
		for section in self.sections:
			data=section.quit()
			if data is not None:
				section._data=data
		self.storeSession()

	def rollback(self):
		"""
		Stops all sections that have already been started.

		If a sessionFile has been set, it stores the data returned by section.quit().
		"""
		for section in self.sections:
			if section._started:
				section.quit()
		self.storeSession()

	def loadSession(self):
		"""
		Stores all data in the sessionFile, if there is one.
		"""
		if self.sessionFile is None:
			return
		try:
			with open(self.sessionFile, "rb") as file:
				data=pickle.load(file)  #Loads list of data
		except (FileNotFoundError, EOFError):
			return
		for i, section in enumerate(self.sections):
			section._data=data[i]

	def storeSession(self):
		"""
		Loads all data from the sessionFile, if there is one.
		"""
		if self.sessionFile is None:
			return
		with open(self.sessionFile, "wb") as file:
			pickle.dump([section._data for section in self.sections],
			            file)   #Stores list of data
