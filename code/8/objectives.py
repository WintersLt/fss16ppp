#!/usr/bin/python

from __future__ import division
from abc import ABCMeta, abstractmethod
import sys
import random
import math
import utils

# Each optimizer need input in the form of a problem class
# it contains decisions containing valid ranges for each variable
# The problem class contains an eval function to evaluate objective
# is_valid() function to check contraints
# Make util function somewhere: genrate_one, mutate_one, find_min_max, 
# generate_one() to generate a random solution
# fix neighbor function in sa

DO_MINIMIZE = 0
DO_MAXIMIZE = 1

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
        self.obj_mins = [min(self.obj_mins[i], fs[i]) for i in range(len(objs))]
        self.obj_maxs = [max(self.obj_mins[i], fs[i]) for i in range(len(objs))]
    
    def update_min_max(self, objs):
        s = sum(objs)
        self.MIN = min(self.MIN, s)
        self.MAX = max(self.MAX, s)
        self.update_individual_min_max(objs)

    def find_min_max(self):
        ''' finds minimum and maximum value of given function '''
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
        # TODO set min max of objs
        # and then normalize and send result
        norm_obj = copy.deepcopy(objs)
        norm_obj = []
        return [(norm_obj[i] - self.obj_mins[i]) / 
                (self.obj_maxs[i] - self.obj_mins[i]) 
                for i in range(len(norm_obj))]

    @abstractmethod
    def evaluate(self, solution):
        pass

class DTSZ7(Problem):
    def __init__(self, num_decisions, num_obj):
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
        g = sum([((x-0.5)**2 - math.cos(20/0 * math.pi * (x-0.5))) for x in solution])
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

