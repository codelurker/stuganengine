#!/usr/bin/env python
import sys
from Game import Game
from Inventory import Inventory
from Room import Room 
from Object import Object
from Action import Action
from Person import Person
from Topic import Topic
from Trigger import Trigger
#TODO: Do the hula hula

Cellar = Room("the Cellar")
CellarDefault = Object("default",[Action("look","You stand in a dark cellar. There is a [window] on the southern wall and a door to the [east]")])
CellarDefault.actions["look"].addTrigger(Trigger('showObject',["cellar","window"]))
Cellar.addObject(CellarDefault)
CellarWindow = Object("window",[Action("look","The window has [bars], so you are unable to look out. The only thing you see are mountains in the distance.")])
CellarWindow.actions["look"].addTrigger(Trigger('showObject',["cellar","bars"]))
Cellar.addObject(CellarWindow)
CellarBars = Object("bars",[Action("look","The bars are made of steel and look very sturdy."),Action("push","Who do you think you are, Superman?")])
Cellar.addObject(CellarBars)
Cellar.exits["east"] = "restroom"

##ADDING SOME DUDE###



Restroom = Room("the Restroom")
RestroomDefault = Object("default",[Action("look","You find yourself in a very small restroom. You notice a bad smell coming from the [toilet]. There is also a worn [sink].")])
RestroomDefault.actions["look"].addTrigger(Trigger("showObject",["restroom","sink"]))
RestroomDefault.actions["look"].addTrigger(Trigger("showObject",["restroom","toilet"]))
Restroom.addObject(RestroomDefault)

RestroomSink = Object("sink",[Action("look","The sink is in a sorry state. There is a tube of [toothpaste] laying on the sink. A bit of it have sipped out and has melted a hole in the sink.")])
RestroomSink.actions["look"].addTrigger(Trigger("showObject",["restroom","toothpaste"]))
Restroom.addObject(RestroomSink)

RestroomToliet = Object("toilet",[Action("look","No. You are not sure you want to do that.")])
#RestroomToliet.actions["look"].addTrigger(Trigger("changeObjectResponse",["restroom","toilet","look","Not being able to resist, you lift the lid of the toilet. That was a bad idea."]))
Restroom.addObject(RestroomToliet)

RestroomToothpaste = Object("toothpaste",[Action("look","You can't make out the brand of the toothpaste, but from what you see it has done to the sink you understand that it must be very strong."),Action("take","You pick up the toothpaste while making very sure not to get anything on you."),Action("use","You put some toothpaste on the bars. They melt away like butter on a sunny day!")])
RestroomToothpaste.actions["take"].addTrigger(Trigger("changeObjectResponse",["restroom","sink","look","The sink is in a sorry state."]))
RestroomToothpaste.actions["use"].target = "bars"
RestroomToothpaste.actions["use"].addTrigger(Trigger("removeObject",["cellar","bars"]))
RestroomToothpaste.actions["use"].addTrigger(Trigger("changeObjectResponse",["cellar","window","look","It has no bars anymore."]))
RestroomToothpaste.actions["use"].addTrigger(Trigger("changeObjectResponse",["cellar","default","look","The cellar is bathing in light coming from the window. With no bars, the [window] on the [south] wall has become an exit. There is also a door to the [east]"]))
RestroomToothpaste.actions["use"].addTrigger(Trigger("setRoomExit",["cellar","south","outside"]))
Restroom.addObject(RestroomToothpaste)
Restroom.exits["west"] = "cellar"


Outside = Room("the Outside")
OutsideDefault = Object("default",[Action("look","You enjoy the sunlight and fresh wind. There is a path to the [west]. There's also an old butler named [Geoffrey] standing here. Ask him about the [weather].")])
Outside.addObject(OutsideDefault)
Outside.exits["north"] = "cellar"

Geoffrey = Person("Geoffrey")
Geoffrey.addTopic(Topic("path","Yeah, that old path leads to the village."))
Geoffrey.addTopic(Topic("toothpaste","Oh? You used the toothpaste to melt the window bars? How ingenious! Where are you going now?"))
Geoffrey.addTopic(Topic("weather","Well, it's a splendid day I'd say! How did you get out of the cellar?"))
Outside.addPerson(Geoffrey)


Game = Game()
Game.inventory = Inventory()

Game.addRoom(Cellar,"cellar");
Game.addRoom(Restroom,"restroom");
Game.addRoom(Outside,"outside");

## Starting Room
StartRoom = "cellar"
if len(sys.argv) > 1 and sys.argv[1] in Game.rooms:
	StartRoom = sys.argv[1]
else:
	exit("Fatal: Not a valid room.")

Game.start(StartRoom)
