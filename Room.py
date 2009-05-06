class Room():
	def __init__(self,name):
		self.game = None
		self.name = name
		self.exits = {}
		self.triggers = {}
		self.triggers["activate"] = {}
		self.triggers["set"] = {}
		self.objects = {}
		self.people = {}

	def __get__(self,var):
		if var in self.objects:
			return self.objects[var]
		else:
			return None

	def hasObject(self,objectName):
		return objectName in self.objects and self.objects[objectName].visible == True
			

	def addObject(self,objectObject):
		objectObject.room = self
		self.objects[objectObject.name] = objectObject

	def removeObject(self,objectObject):
		del self.objects[objectObject.name]

	def addPerson(self,personObject):
		personObject.room = self
		self.people[personObject.name] = personObject
		print "Added",personObject.name,"to",self.name

	def setObjectVisibility(self,objectName,visible=True):
		if objectName in self.objects:
			self.objects[objectName].visible = visible

	def enter(self):
		print 45*"\n"
		print "Entering",self.name

	def addTrigger(self,trigger,type,object):
		self.triggers[type][trigger] = object
