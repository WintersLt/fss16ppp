#!/usr/bin/python

from __future__ import division
from abc import ABCMeta, abstractmethod
import sys
import random
import math
import utils
import copy
from ga import ga

DO_MINIMIZE = 0
DO_MAXIMIZE = 1

# Objective function and ancillaries for using GA objective of DE
class GAPoint(object):
	id = 0
	def __init__(self, decisions, problem):
		GAPoint.id += 1
		self.decisions = decisions
		self.problem = problem
		self.obj = None
		self.id = GAPoint.id
	def evaluate(self):
		if not self.obj:
			self.obj = self.problem.evaluate(self.decisions)
		return self.obj

class GADecision(object):
    def __init__(self, name, vals):
        self.name = name
        self.vals = vals

    def any(self):
        return self.vals[random.randint(0, len(self.vals)-1)]

class GAProblemBase(object):
    """
    Class representing the problem.
    """
    def __init__(self):
        __metaclass__ = ABCMeta
        self.obj_mins = []
        self.obj_maxs = []
        self.objective_type = []
        self.MIN = None
        self.MAX = None

    @abstractmethod
    def is_valid(self, solution):
        pass
    def update_individual_min_max(self, objs):
    	if not len(self.obj_mins):
    		self.obj_mins = objs
    		self.obj_maxs = objs
    		return
        self.obj_mins = [min(self.obj_mins[i], objs[i]) for i in range(len(objs))]
        self.obj_maxs = [max(self.obj_maxs[i], objs[i]) for i in range(len(objs))]
    
    def update_min_max(self, obj):
        self.MIN = min(self.MIN, obj)
        self.MAX = max(self.MAX, obj)

    def find_min_max(self):
        ''' finds minimum and maximum value of given function '''
    	if self.MIN: return self.MIN, self.MAX
        sol = self.generate_one()
        self.MIN = self.MAX = self.evaluate(sol)
        for i in range(10):
            sol = self.generate_one()
            objs = self.evaluate(sol)
            self.update_min_max(objs)
        return self.MIN, self.MAX

    def generate_one(self):
        max_ret = 10000
        i = 0
        while(i<max_ret):
            sol = [self.decisions[i].any() for i in range(len(self.decisions))]
            if self.is_valid(sol):
                return sol
            i+=1
        print "Error generate_one(): couldnt generate solution"
        return None
    
    def normalise_obj(self, obj):
        return (obj - self.MIN) / (self.MAX - self.MIN) 

    @abstractmethod
    def evaluate(self, solution):
        pass

class GAProblem(GAProblemBase):
    def __init__(self, problem):
        GAProblemBase.__init__(self)
        self.decisions = [ GADecision("Mutations", [0.01, 0.05, 0.15]),
                           GADecision("Crossover", ["single_pt", "two_pt", "uniform"]),
						   GADecision("Select", ["nsga2bdom", "nsga2cdom", "gacdom"]),
						   GADecision("Size", [40, 70, 100]),
						   GADecision("Generations", [25, 35, 45])]
        self.objective_type = [DO_MINIMIZE]
    	self.problem = problem
    	self.evaluate_cache = {} # parame to evaluate() value
    	self.init_hve_cache = None # init hve only depends upon problem type
    def is_valid(self, solution):
        return True

    def get_objectives(self, solution):
    	self.init_hve_cache, hvol = ga(self.problem, pop_size = solution[3], 
				gens = solution[4], select_type = solution[2], mutation_rate = solution[0],
				crossover_type = solution[1], init_hve = self.init_hve_cache)
    	self.update_min_max(hvol)
        return hvol

    def evaluate(self, solution):
    	sol_str = str(solution)
    	if sol_str in self.evaluate_cache:
    		return self.evaluate_cache[sol_str]
        v = self.get_objectives(solution)
    	self.evaluate_cache[sol_str] = v
    	return v

## Mathematical objective functions
class Decision(object):
    def __init__(self, name, low, high):
        self.name = name
        self.low = low
        self.high = high

    def any(self):
        return self.low + utils.r()*(self.high - self.low)

class Problem(object):
    """
    Class representing the problem.
    """
    def __init__(self):
        __metaclass__ = ABCMeta
        self.obj_mins = []
        self.obj_maxs = []
        self.objective_type = []
        self.MIN = None
        self.MAX = None

    @abstractmethod
    def is_valid(self, solution):
        pass
    def update_individual_min_max(self, objs):
    	if not len(self.obj_mins):
    		self.obj_mins = objs
    		self.obj_maxs = objs
    		return
        self.obj_mins = [min(self.obj_mins[i], objs[i]) for i in range(len(objs))]
        self.obj_maxs = [max(self.obj_maxs[i], objs[i]) for i in range(len(objs))]
    
    def update_min_max(self, objs):
        s = sum(objs)
        self.MIN = min(self.MIN, s)
        self.MAX = max(self.MAX, s)
        self.update_individual_min_max(objs)

    def find_min_max(self):
        ''' finds minimum and maximum value of given function '''
    	if self.MIN: return self.MIN, self.MAX
        sol = self.generate_one()
        self.MIN = self.MAX = self.evaluate(sol)
        self.obj_mins = self.obj_maxs = self.get_objectives(sol)
        for i in range(100):
            sol = self.generate_one()
            objs = self.get_objectives(sol)
            self.update_min_max(objs)
        return self.MIN, self.MAX


    def generate_one(self):
        max_ret = 10000
        i = 0
        while(i<max_ret):
            sol = [self.decisions[i].any() for i in range(len(self.decisions))]
            if self.is_valid(sol):
                return sol
            i+=1
        print "Error generate_one(): couldnt generate solution"
        return None
    
    def normalise_obj(self, objs):
        return [(objs[i] - self.obj_mins[i]) / 
                (self.obj_maxs[i] - self.obj_mins[i]) 
                for i in range(len(objs))]

    @abstractmethod
    def evaluate(self, solution):
        pass

class DTSZ7(Problem):
    def __init__(self, num_decisions, num_obj):
        Problem.__init__(self)
        self.decisions = [Decision('x' + str(i+1), 0, 1) for i in range(num_decisions)]
        self.num_obj = num_obj
        self.num_decisions = num_decisions
        self.objective_type = [DO_MINIMIZE for _ in range(num_obj)]
    def is_valid(self, solution):
        return True

    # Inspired from Jmetal
    # https://github.com/jMetal/jMetal/blob/master/jmetal-problem/src/main/java/org/uma/jmetal/problem/multiobjective/dtlz/DTLZ7.java
    def get_objectives(self, solution):
        f = solution[0 : (self.num_obj-1)]
        k = self.num_decisions - self.num_obj + 1
        g = sum(solution[(self.num_decisions - k):])
        g = 1 + (9.0 * g) / k
        h = sum([(fi / (1.0 + g))*(1+math.sin(3.0 * math.pi * fi)) for fi in f])
        h = self.num_obj - h
        f += [(1+g)*h]
        self.update_min_max(f)
        return f

    def evaluate(self, solution):
        return sum(self.get_objectives(solution))


class DTSZ1(Problem):
    def __init__(self, num_decisions, num_obj):
        Problem.__init__(self)
        self.decisions = [Decision('x' + str(i+1), 0, 1) for i in range(num_decisions)]
        self.num_obj = num_obj
        self.num_decisions = num_decisions
        self.objective_type = [DO_MINIMIZE for _ in range(num_obj)]

    def is_valid(self, solution):
        return True

    # Inspired from Jmetal
    # https://github.com/jMetal/jMetal/blob/master/jmetal-problem/src/main/java/org/uma/jmetal/problem/multiobjective/dtlz/DTLZ1.java
    def get_objectives(self, solution):
        k = self.num_decisions - self.num_obj + 1
        g = sum([((x-0.5)**2 - math.cos(20.0 * math.pi * (x-0.5))) for x in solution])
        g = 100 * (k+g)
        f = [(1.0 + g)*0.5] * self.num_obj
        for i in xrange(self.num_obj-1):
            for j in xrange(self.num_obj - i - 1):
                f[i] *= solution[j]
            if i != 0:
                aux = self.num_obj - (i+1)
                f[i] *= 1 - solution[aux]
        self.update_min_max(f)
        return f

    def evaluate(self, solution):
        return sum(self.get_objectives(solution))


class DTSZ3(Problem):
    def __init__(self, num_decisions, num_obj):
        Problem.__init__(self)
        self.decisions = [Decision('x' + str(i+1), 0, 1) for i in range(num_decisions)]
        self.num_obj = num_obj
        self.num_decisions = num_decisions
        self.objective_type = [DO_MINIMIZE for _ in range(num_obj)]

    def is_valid(self, solution):
        return True

    # Inspired from Jmetal
    # https://github.com/jMetal/jMetal/blob/master/jmetal-problem/src/main/java/org/uma/jmetal/problem/multiobjective/dtlz/DTLZ3.java
    def get_objectives(self, solution):
        k = self.num_decisions - self.num_obj + 1
        g = sum([((x-0.5)**2 - math.cos(20.0 * math.pi * (x-0.5))) for x in solution])
        g = 100 * (k+g)
        f = [(1.0 + g)] * self.num_obj
        for i in xrange(self.num_obj-1):
            for j in xrange(self.num_obj - i - 1):
                f[i] *= math.cos(solution[j] * 0.5 * math.pi)
            if i != 0:
                aux = self.num_obj - (i+1)
                f[i] *= math.sin(solution[aux] * 0.5 * math.pi)
        self.update_min_max(f)
        return f

    def evaluate(self, solution):
        return sum(self.get_objectives(solution))

class DTSZ5(Problem):
    def __init__(self, num_decisions, num_obj):
        Problem.__init__(self)
        self.decisions = [Decision('x' + str(i+1), 0, 1) for i in range(num_decisions)]
        self.num_obj = num_obj
        self.num_decisions = num_decisions
        self.objective_type = [DO_MINIMIZE for _ in range(num_obj)]

    def is_valid(self, solution):
        return True

    # Inspired from Jmetal
    # https://github.com/jMetal/jMetal/blob/master/jmetal-problem/src/main/java/org/uma/jmetal/problem/multiobjective/dtlz/DTLZ5.java
    def get_objectives(self, solution):
        k = self.num_decisions - self.num_obj + 1
        g = sum([(x-0.5)**2 for x in solution])
        t = math.pi / (4.0 * (1.0 + g))
        theta = []
        theta.append(solution[0] * math.pi / 2.0)
        for i in xrange(self.num_obj - 1 - 1):
            theta.append(t * (1.0 + 2.0 * g * solution[i+1]))
        f = [1.0 + g] * self.num_obj
        
        for i in xrange(self.num_obj-1):
            for j in xrange(self.num_obj - i - 1):
                f[i] *= math.cos(theta[j])
            if i != 0:
                aux = self.num_obj - (i+1)
                f[i] *= math.sin(theta[aux])
        self.update_min_max(f)
        return f

    def evaluate(self, solution):
        return sum(self.get_objectives(solution))

