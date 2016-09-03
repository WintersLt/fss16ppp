import math;
from swampy.TurtleWorld import *


world = TurtleWorld()
bob = Turtle()
bob.delay =0.01
print bob

def square(bob, len=100):
	for _ in range(4):	
		fd(bob, len)
		lt(bob)
	
	

def polygon(bob, n, length=100):

	angle = 360.0/n;
	for _ in range(n):
		fd(bob, length)
		lt(bob,angle)
	
	

def polygon_with_dia(bob,n,length=100):

	angle = 180 - 360.0/n;
	dia_angle = 180 - angle/2;	
	radius = length / (2 * math.sin(math.radians(180/n)))
	
	for _ in range(n):		
		fd(bob, length)
		lt(bob, dia_angle)
		fd(bob, radius)
		lt(bob, 180)
		fd(bob, radius)
		lt(bob, dia_angle)
		

#polygon_with_dia(bob, 5, 50)
#polygon_with_dia(bob, 6, 50)
polygon_with_dia(bob, 8, 50)

#def circle(t, radius):
#	circum = 2* math.pi * radius
#	length = circum/360	
#	polygon(t,360,length)	


def circle(t,radius,arc= 360):
	circum = 2* math.pi * radius
	length = circum/360	
	for _ in range(arc):
		polygon(t,1,length)
		lt(t,1)
	

def petal(t, radius, angle):
	
	for i in range(2):
		circle(t,radius, angle)
		lt(t, 180 - angle)



def flowers(t, n, radius, angle):
	for i in range(n):
		petal(t, radius, angle)
		lt(t, 360.0/n)

#flowers(bob, 7, 60, 60)	
#flowers(bob, 10, 40, 80)
#flowers(bob, 20, 140, 20)

#circle(bob,50)
#circle(bob,50,180)

#polygon(bob, 10, 25)	

#square(bob,10)
	

wait_for_user()
