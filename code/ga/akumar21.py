
# All the imports
from __future__ import print_function, division
from math import *
import random
import sys
import matplotlib.pyplot as plt

# TODO 1: Enter your unity ID here 
__author__ = "akumar21"

class O:
    """
    Basic Class which
        - Helps dynamic updates
        - Pretty Prints
    """
    def __init__(self, **kwargs):
        self.has().update(**kwargs)
    def has(self):
        return self.__dict__
    def update(self, **kwargs):
        self.has().update(kwargs)
        return self
    def __repr__(self):
        show = [':%s %s' % (k, self.has()[k]) 
                for k in sorted(self.has().keys()) 
                if k[0] is not "_"]
        txt = ' '.join(show)
        if len(txt) > 60:
            show = map(lambda x: '\t' + x + '\n', show)
        return '{' + ' '.join(show) + '}'
    
print("Unity ID: ", __author__)


# Few Utility functions
def say(*lst):
    """
    Print whithout going to new line
    """
    print(*lst, end="")
    sys.stdout.flush()

def random_value(low, high, decimals=2):
    """
    Generate a random number between low and high. 
    decimals incidicate number of decimal places
    """
    return round(random.uniform(low, high),decimals)

def gt(a, b): return a > b

def lt(a, b): return a < b

def shuffle(lst):
    """
    Shuffle a list
    """
    random.shuffle(lst)
    return lst

class Decision(O):
    """
    Class indicating Decision of a problem
    """
    def __init__(self, name, low, high):
        """
        @param name: Name of the decision
        @param low: minimum value
		@param high: maximum value
        """
        O.__init__(self, name=name, low=low, high=high)
        
class Objective(O):
    """
    Class indicating Objective of a problem
    """
    def __init__(self, name, do_minimize=True):
        """
        @param name: Name of the objective
        @param do_minimize: Flag indicating if objective has to be minimized or maximized
        """
        O.__init__(self, name=name, do_minimize=do_minimize)

class Point(O):
    """
    Represents a member of the population
    """
    def __init__(self, decisions):
        O.__init__(self)
        self.decisions = decisions
        self.objectives = None
        
    def __hash__(self):
        return hash(tuple(self.decisions))
    
    def __eq__(self, other):
        return self.decisions == other.decisions
    
    def clone(self):
        new = Point(self.decisions)
        new.objectives = self.objectives
        return new

class Problem(O):
    """
    Class representing the cone problem.
	"""
    def __init__(self):
        O.__init__(self)
        # TODO 2: Code up decisions and objectives below for the problem
        # using the auxilary classes provided above.
        self.decisions = [ Decision("radius",0,10), Decision("height", 0, 20)]
        self.objectives = [Objective("S",True), Objective("T", True)]
        
    @staticmethod
    def evaluate(point):
        [r, h] = point.decisions
        point.objectives = []
        # TODO 3: Evaluate the objectives S and T for the point.
        l = (r**2 + h**2)**0.5
        S =pi *r*l
        T = pi*r*(r+l)
        point.objectives = [S,T]
        #print ("obj = ", str(point.objectives))
        return point.objectives
    
    @staticmethod
    def is_valid(point):
        [r, h] = point.decisions
        # TODO 4: Check if the point has valid decisions
        V = pi*(r**2)*h/3
        return V > 200
    
    def generate_one(self):
        # TODO 5: Generate a valid instance of Point.
        while(True):
            point = Point([random_value(d.low, d.high) for d in self.decisions])
            if self.is_valid(point):
				return point
        
cone = Problem()
point = cone.generate_one()
cone.evaluate(point)
#print(point)



def populate(problem, size):
    population = []
    # TODO 6: Create a list of points of length 'size'
    for _ in xrange(size):
        population.append(problem.generate_one())
    return population

#print(populate(cone,5))

def crossover(mom, dad):
    # TODO 7: Create a new point which contains decisions from 
    # the first half of mom and second half of dad
    n = len(mom.decisions)    
    return Point(mom.decisions[:n//2] + dad.decisions[n//2:])

def mutate(problem, point, mutation_rate=0.01):
    # TODO 8: Iterate through all the decisions in the point
    # and if the probability is less than mutation rate
    # change the decision(randomly set it between its max and min).
    for i, decision in enumerate(problem.decisions):
        if random.random() < mutation_rate:
            point.decisions[i] = random_value(decision.low, decision.high)
    return point

def bdom(problem, one, two):
    """
    Return if one dominates two
    """
    objs_one = problem.evaluate(one)
    objs_two = problem.evaluate(two)
    dominates = False    
    # TODO 9: Return True/False based on the definition
    # of bdom above.
    
    for i, obj in enumerate(objs_one):
        if (objs_one[i] > objs_two[i]):
            return False
        elif (objs_one[i] < objs_two[i]):
            dominates = True        

    return dominates

def fitness(problem, population, point):
    dominates = 0
    # TODO 10: Evaluate fitness of a point.
    # For this workshop define fitness of a point 
    # as the number of points dominated by it.
    # For example point dominates 5 members of population,
    # then fitness of point is 5.
    for p in population:
        if (bdom(problem,point, p)):
            dominates = dominates + 1
    return dominates

def elitism(problem, population, retain_size):
    # TODO 11: Sort the population with respect to the fitness
    # of the points and return the top 'retain_size' points of the population

    population = sorted(population, key = lambda p: fitness(problem,population, p), reverse= True)

    return population[:retain_size]

def ga(pop_size = 100, gens = 250):
    problem = Problem()
    population = populate(problem, pop_size)
    [problem.evaluate(point) for point in population]
    initial_population = [point.clone() for point in population]
    gen = 0 
    while gen < gens:
        say(".")
        children = []
        for _ in range(pop_size):
            mom = random.choice(population)
            dad = random.choice(population)
            while (mom == dad):
                dad = random.choice(population)
            child = mutate(problem, crossover(mom, dad))
            if problem.is_valid(child) and child not in population+children:
                children.append(child)
        population += children
        population = elitism(problem, population, pop_size)
        gen += 1
    print("")
    return initial_population, population

def plot_pareto(initial, final):
    initial_objs = [point.objectives for point in initial]
    final_objs = [point.objectives for point in final]
    initial_x = [i[0] for i in initial_objs]
    initial_y = [i[1] for i in initial_objs]
    final_x = [i[0] for i in final_objs]
    final_y = [i[1] for i in final_objs]
    plt.scatter(initial_x, initial_y, color='b', marker='+', label='initial')
    plt.scatter(final_x, final_y, color='r', marker='o', label='final')
    plt.title("Scatter Plot between initial and final population of GA")
    plt.ylabel("Total Surface Area(T)")
    plt.xlabel("Curved Surface Area(S)")
    plt.legend(loc=9, bbox_to_anchor=(0.5, -0.175), ncol=2)
    plt.show()

initial, final = ga()
plot_pareto(initial, final)
