class Object():
	def __init__(self,name,actions = {}):
		self.room = None
		self.name = name
		self.actions = {}

		#Force user to discover all objects
		if name == "default":
			self.visible = True
		else:
			self.visible = False

		for action in actions:
			self.addAction(action)

	def __get__(self,var):
		if var in self.actions:
			 return self.actions[var]
		else:
			return None

	def hasAction(self,actionName):
		return actionName in self.actions

	def addAction(self,actionObject):
		actionObject.object = self
		self.actions[actionObject.type] = actionObject

	def remove(self):
		self.room.removeObject(self)
		self = None
