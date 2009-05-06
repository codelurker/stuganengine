class Person():
	def __init__(self,name,topics={}):
		self.name = name
		self.topics = {}
		for topic in topics:
			self.addTopic(topic)			

	def addTopic(self,topicObject):
		self.topics[topicObject.name.lower()] = topicObject
