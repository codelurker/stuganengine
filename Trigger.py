class Trigger:
	def __init__(self,type=None,args=None):
		self.action = None
		self.game = None
		self.type = type
		self.args = args
		self.triggered = False
		self.preserve = False

	def run(self):
		if not self.triggered or self.preserve:
			if self.type != None and self.args != None and self.type in ['changeObjectResponse','removeObject','showObject','hideObject','execCode','setRoomExit']:
				execString = "self."+self.type+"("
				for argument in self.args:
					execString += "\""+argument+"\","
				execString = execString[:-1]
				execString += ")"
				print "###",execString
				exec(execString)
				self.triggered = True
			else:
				print "### FAILED TO RUN",self.type,"###"

	def showObject(self,roomKey,objectKey):
		self.action.object.room.game.rooms[roomKey].setObjectVisibility(objectKey,True)

	def hideObject(self,roomKey,objectKey):
		self.action.object.room.game.rooms[roomKey].setObjectVisibility(objectKey,False)

	def removeObject(self,roomKey,objectKey):
		self.action.object.room.game.rooms[roomKey].objects[objectKey].remove()

	def changeObjectResponse(self,roomKey,objectKey,actionKey,response):
		self.action.object.room.game.rooms[roomKey].objects[objectKey].actions[actionKey].response = response
		#LOL OH MY GOD SOMEONE PUNISH ME!

	def setRoomExit(self,roomKey,direction,newRoomKey):
		self.action.object.room.game.rooms[roomKey].exits[direction] = newRoomKey

