import cmd
import string, sys

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

	def do_ask(self,askString):
		askString = askString.lower()
		askPerson = None
		askTopic = None

		if "about" in askString:
			for person in self.currentRoom.people:
				if askString.startswith(person.lower()):
					askPerson = self.currentRoom.people[person]

			if askPerson != None:

				for topic in askPerson.topics:
					if askString.endswith(topic.lower()):
						askTopic = askPerson.topics[topic]
		else:
			print "Hm, what?"
			return

		if askPerson != None and askTopic != None:
			print askTopic.reply
		else:
			"Nope."
			
	def do_quit(self, arg):
		exit("Bye!")

	do_q = do_quit

	def do_dump(self, arg):
		print self.inventory.items
