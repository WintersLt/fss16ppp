class Employee:
	''' An Employee class '''
	def __init__(self, name, age):
		self.name = name
		self.age = age

	def __repr__(i):
		return i.__class__.__name__+" " + i.name + " " + str(i.age)

	def __lt__(self, other):
		return self.age < other.age


ram = Employee("ram ", 50)
mohan = Employee(" mohan ",30)

employees = [ram, mohan]
print "Before Sorting", employees
employees.sort()
print "After Sorting", employees
