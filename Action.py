class Action():
	def __init__(self,type,response=None,):
		self.object = None
		self.type = type
		self.response = response
		self.switch = None
		self.shows = None
		self.hides = None
		self.target = None
		self.code = None
		self.triggers = []

	def addTrigger(self,triggerObject):
		triggerObject.action = self
		self.triggers.append(triggerObject)

	def run(self):

		if len(self.triggers) > 0:
			for trigger in self.triggers:
				trigger.run()

		if self.type == "use" and self.object.room.game.inventory.hasItem(self.object):
			self.object.room.game.inventory.removeItem(self.object)

		if self.type == "take":
			#Hide taken objects
			self.object.visible=False
			self.object.room.game.inventory.addItem(self.object)

		if self.response != None:
			print 45*"\n"
			print self.response
