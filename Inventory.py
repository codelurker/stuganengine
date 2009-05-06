class Inventory():

	def __init__(self):
		self.items = {}
	
	def addItem(self,object):
		self.items[object.name.lower()] = object

	def removeItem(self,object):
		self.items.pop(object.name)

	def hasItem(self,object):
		print object
		return object in self.items

	def listItems(self):
		if len(self.items) > 0:
			for item in self.items:
				print "*",self.items[item].name
