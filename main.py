#!/usr/bin/env python
import cmd
import string, sys

class Action():
	def __init__(self,type,response=None):
		self.object = None
		self.type = type
		self.response = response
		self.switch = None
		self.shows = None
		self.hides = None
		self.target = None

	def run(self):

		if self.type == "use" and self.object.room.game.inventory.hasItem(self.object):
			self.object.room.game.inventory.removeItem(self.object)

		if self.type == "take":
			self.object.room.game.inventory.addItem(self.object)

		if self.switch != None:
			print "I wanna set",self.switch

		if self.shows != None:
			for objectName in self.shows:
				self.object.room.setObjectVisibility(objectName,True)

		if self.hides != None:
			for objectName in self.hides:
				self.object.room.setObjectVisibility(objectName,False)

		if self.response != None:
			print self.response

		self.special()

	def special(self):
		#To be overwritten with special functions
		return

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

class Room():
	def __init__(self,name):
		self.game = None
		self.name = name
		self.exits = {}
		self.triggers = {}
		self.triggers["activate"] = {}
		self.triggers["set"] = {}
		self.objects = {}

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

	def setObjectVisibility(self,objectName,visible=True):
		if objectName in self.objects:
			self.objects[objectName].visible = visible

	def enter(self):
		print "Entering",self.name

	def addTrigger(self,trigger,type,object):
		self.triggers[type][trigger] = object


class Inventory():

	def __init__(self):
		self.items = {}
	
	def addItem(self,object):
		self.items[object.name.lower()] = object

	def removeItem(self,object):
		print self.items[object]
		self.items.pop(object)

	def hasItem(self,objectName):
		return objectName in self.items

	def listItems(self):
		if len(self.items) > 0:
			#WTF IS THIS? IT'S NOT SUPPOSED TO BE THIS HARD
			for item in self.items.keys():
				print "*",self.items[item].name

class Game(cmd.Cmd):

	def __init__(self):
		cmd.Cmd.__init__(self)
		self.prompt = "> "
		self.rooms = {}
		self.currentRoom = ""
		self.switches = []

	def default(self,line):
		print "You can't do that here."
	
	def start(self,roomKey=None):
		if roomKey != None:
			self.enterRoom(roomKey)
			self.cmdloop()
		else:
			exit("Fatal Error: There is no room to enter.")

	def runTriggers(self,triggerKey):
		if triggerKey in self.currentRoom.triggers["activate"]:
			self.currentRoom.enableObject(self.currentRoom.triggers["activate"][triggerKey])
			
		if triggerKey in self.currentRoom.triggers["set"]:
			self.switches.append(self.currentRoom.triggers["set"][triggerKey])

	def addRoom(self,roomObject,roomKey):
		roomObject.game = self
		self.rooms[roomKey] = roomObject

	def enterRoom(self,roomKey):
		if roomKey != "" and roomKey in self.rooms:
			self.currentRoom = self.rooms[roomKey]
			self.currentRoom.enter()
		else:
			#Bug
			print "The door is locked."

	def do_look(self, object):
		if object == "": object="default"

		if self.currentRoom.hasObject(object) and self.currentRoom.objects[object].hasAction("look"):
			self.currentRoom.objects[object].actions["look"].run()
		else:
			if object == "default":
				print "There is nothing to see here."
			else:
				print "What is",object,"?"


	def do_push(self, object):
		if object != "":
			if self.currentRoom.hasObject(object):
				if self.currentRoom.objects[object].hasAction("push"):
					self.currentRoom.objects[object].actions["push"].run()
				else:
					print "You can't push that."
			else:
				print "What is",object,"?"

	def do_take(self, object):
		if object != "":
			if self.currentRoom.hasObject(object):
				if self.currentRoom.objects[object].hasAction("take"):
					self.currentRoom.objects[object].actions["take"].run()
				else:
					print "You can't take that."
			else:
				if self.inventory.hasItem(object):
					print "You already have it."
				else:
					print "What is",object,"?"

	def do_go(self, direction):
		if direction == "e": direction = "east"
		if direction == "w": direction = "west"
		if direction == "n": direction = "north"
		if direction == "s": direction = "south"

		if direction in self.currentRoom.exits:
			self.enterRoom(self.currentRoom.exits[direction])
		else:
			print "You can't go in that direction."

	def do_inventory(self,item):
		self.inventory.listItems()

	def do_use(self,useString):
		useString = useString.lower()
		useItem = None
		useObject = None

		if "with" in useString or "on" in useString:
			for item in self.inventory.items:
				if useString.startswith(item.lower()) and self.inventory.items[item].hasAction("use"):
					useItem = item

			for object in self.currentRoom.objects:
				if useString.endswith(object.lower()) and self.currentRoom.objects[object].visible == True:
					useObject = object
		else:
			print "Hm, what?"
			return

		if useItem != None:
			if useObject != None:
				if useObject.lower() == self.inventory.items[item].actions["use"].target.lower():
					self.inventory.items[item].actions["use"].run()
				else: 
					print "You can't use that item for that"
			else:
				print "Where do you want to use that?"
		else: 
			print "You can't use what you don't have"

	def do_quit(self, arg):
		exit("Bye!")

	do_q = do_quit

	def do_dump(self, arg):
		print self.currentRoom.objects["default"].actions["look"].response

Cellar = Room("the Cellar")
cellarDefault = Object("default",[Action("look","You stand in a dark cellar. There is a [window] on the eastern wall and a door to the [east]")])
cellarDefault.actions["look"].shows = ["window"]
Cellar.addObject(cellarDefault)
cellarWindow = Object("window",[Action("look","The window has [bars], so you are unable to look out. The only thing you see are mountains in the distance.")])
cellarWindow.actions["look"].shows = ["bars"]
Cellar.addObject(cellarWindow)
cellarBars = Object("bars",[Action("look","The bars are made of steel and look very sturdy."),Action("push","Who do you think you are, Super man?")])
Cellar.addObject(cellarBars)
Cellar.exits["east"] = "Restroom"

Restroom = Room("the Restroom")
restroomDefault = Object("default",[Action("look","You find yourself in a very small restroom. You notice a bad smell coming from the [toilet]. There is also a worn [sink].")])
restroomDefault.actions["look"].shows = ["sink","toilet"]
Restroom.addObject(restroomDefault)

restroomSink = Object("sink",[Action("look","The sink is in a sorry state. There is a tube of [toothpaste] lying on the sink. A bit of it have sipped out and has melted a hole in the sink.")])
restroomSink.actions["look"].shows = ["toothpaste"]
Restroom.addObject(restroomSink)

restroomToliet = Object("toilet",[Action("look","No. You do not want to do that.")])
Restroom.addObject(restroomToliet)

restroomToothpaste = Object("toothpaste",[Action("look","You can't make out the brand of the toothpaste, but from what you see it has made to the sink you understand that it must be very strong."),Action("take","You pick up the toothpaste while making very sure not to get anything on you."),Action("use","You put some toothpaste on the bars. They melt away like butter on a sunny day!")])
restroomToothpaste.actions["take"].hides = ["toothpaste"]
restroomToothpaste.actions["use"].target = "bars"


Restroom.addObject(restroomToothpaste)
Restroom.exits["west"] = "Cellar"



'''
cellarWindow = Object("window",[Action("look","The window has [bars], so you are unable to look out. The only thing you see are mountains in the distance.")])
cellarWindow.actions["look"].shows = "bars"
Cellar.addObject(cellarWindow)
cellarBars = Object("bars",[Action("look","The bars are made of steel and look very sturdy."),Action("push","Who do you think you are, Super man?")])
cellarBars.visible = False
Cellar.addObject(cellarBars)
Cellar.exits["east"] = "Toilet"
'''

#Cellar.objects["window"]

Game = Game()
Game.inventory = Inventory()

Game.inventory.addItem(restroomToothpaste)
Game.addRoom(Cellar,"Cellar");
Game.addRoom(Restroom,"Restroom");

Game.start("Cellar")

