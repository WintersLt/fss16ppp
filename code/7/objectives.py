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

    @abstractmethod
    def is_valid(self, solution):
        pass

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
    
    @abstractmethod
    def evaluate(self, solution):
        pass
 
class Schaffer(Problem):
    def __init__(self):
        self.decisions = [Decision("x", -10000.0, 10000.0)]
    def is_valid(self, solution):
        return True
    def evaluate(self, solution):
        [x] = solution
        return (x*x) + (x-2)*(x-2)

class Osyczka2(Problem):
    def __init__(self):
        self.decisions = [Decision('x1', 0, 10), Decision('x2', 0, 10),
                          Decision("x3", 1, 5), Decision("x4", 0, 6), 
                          Decision("x5", 1, 5), Decision("x6", 0, 10)]
    def is_valid(self, solution):
        [x1, x2, x3, x4, x5, x6] = solution
        g1 = x1 + x2 - 2
        g2 = 6 - x1 - x2
        g3 = 2 - x2 + x1
        g4 = 2 - x1 + 3*x2
        g5 = 4 - (x3-3)**2 - x4
        g6 = (x5-3)**3 + x6 - 4
        if g1>=0 and g2>=0 and g3>=0 and g4>=0 and g5>=0 and g6>=0:
            return True
        return False
    def evaluate(self, solution):
        '''Calculates the value of osckyza function'''
        [x1, x2, x3, x4, x5, x6] = solution
        f1 = -25*((x1 - 2)**2) + (x2-2)**2 + ((x3-1)**2)*((x4-4)**2) + (x5-1)**2
        f2 = x1**2 + x2**2 + x3**2 + x4**2 + x5**2 + x6**2
        return f1+f2

class Kursawe(Problem):
    def __init__(self):
        self.n = 3
        self.a = 0.8 
        self.b = 1
        self.decisions = [Decision("x%d" %i, -5.0, 5.0) for i in range(self.n)]
    def is_valid(self, solution):
        return True
    def evaluate(self, solution):
        f1 = sum([-10 * math.exp(-0.2 * math.sqrt(solution[i]**2 + solution[i+1]**2)) for i in range(self.n-1)])
        f2 = sum([abs(solution[i])**self.a + 5*(math.sin(solution[i]))**self.b for i in range(self.n)])
        return f1 + f2

class DTSZ7(Problem):
    def __init__(self, num_decisions, num_obj):
        self.decisions = [Decision('x' + str(i+1), 0, 1) for i in range(num_decisions)]
        self.num_obj = num_obj
        self.num_decisions = num_decisions
    def is_valid(self, solution):
        return True
    def evaluate(self, solution):
        f = solution[0 : (self.num_obj-1)]
        k = self.num_decisions - self.num_obj + 1
        g = sum(solution[(self.num_decisions - k):])
        g = 1 + (9.0 * g) / k
        h = sum([(fi / (1.0 + g))*(1+math.sin(3.0 * math.pi * fi)) for fi in f])
        h = self.num_obj - h
        f += [(1+g)*h]
        return sum(f)
