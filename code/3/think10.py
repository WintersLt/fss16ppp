

def has_duplicates(t):
	newList = list(t)
	newList.sort()
	duplicateFlag = False
	for i in range(1, len(newList)):
		if (newList[i-1] == newList[i]):
			duplicateFlag = True
			break
	return duplicateFlag


nl = [1,6,2,3,9,6]
print "given list ", nl
print "has duplicates", has_duplicates(nl)	


import random

def generateRandomBdayList():
	bdayList = []
	for i in range(23):
		bday = random.randint(1,365)
		bdayList.append(bday)
	return bdayList



simulationCount = 10000
print "simulation count = ", simulationCount
count =0
for i in range(simulationCount):
	bdayList = generateRandomBdayList()
	hasDup = has_duplicates(bdayList)
	if(hasDup == True):
		count = count+1

prob = count/float(simulationCount)
print "probability = ", prob
	
