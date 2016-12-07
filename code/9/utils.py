#!/usr/bin/python

from __future__ import division
import sys
import random
import math
import objectives

''' Util functions '''

def generate_one(problem):
    max_ret = 10000
    i = 0
    while(i<max_ret):
        sol = [problem.decisions[i].any() for i in range(len(problem.decisions))]
        if problem.is_valid(sol):
            return sol
        i+=1
    print "Error generate_one(): couldnt generate solution"
    return None

def update_individual_min_max(problem, solution):
	fs = problem.get_objectives(solution)
	problem.obj_mins = [min(problem.obj_mins[i], fs[i]) for i in range(len(fs))]
	problem.obj_maxs = [max(problem.obj_maxs[i], fs[i]) for i in range(len(fs))]


def find_min_max(problem):
    ''' finds minimum and maximum value of given function '''
    sol = generate_one(problem)
    low = high = problem.evaluate(sol)
    problem.obj_mins = problem.obj_maxs = problem.get_objectives(sol)
    for i in range(100):
        sol = generate_one(problem)
        s = problem.evaluate(sol)
        if s<low :
            low = s
        if s>high :
            high = s
    	update_individual_min_max(problem, sol)
	problem.MIN, problem.MAX = low, high
    return low, high

def r(): 
    return random.random()

def cdom(problem, one, other):
    one_to_other = 0.0
    other_to_one = 0.0
    normalised_one = problem.normalise_obj(one)
    normalised_other = problem.normalise_obj(other)
    for i in range(len(one)):
        obj1 = normalised_one[i]
        obj2 = normalised_other[i]
        w = -1 if problem.objective_type[i] == objectives.DO_MINIMIZE else 1
        one_to_other += (-1 * math.e**( w * (obj1 - obj2)/len(one)))
        other_to_one += (-1 * math.e**( w * (obj2 - obj1)/len(one)))
    return one_to_other < other_to_one # remember both quantities are negative

def cdom_loss(problem, one, other):
    one_to_other = 0.0
    other_to_one = 0.0
    normalised_one = problem.normalise_obj(one)
    normalised_other = problem.normalise_obj(other)
    for i in range(len(one)):
        obj1 = normalised_one[i]
        obj2 = normalised_other[i]
        w = -1 if problem.objective_type[i] == objectives.DO_MINIMIZE else 1
        one_to_other += (-1 * math.e**( w * (obj1 - obj2)/len(one)))
        other_to_one += (-1 * math.e**( w * (obj2 - obj1)/len(one)))
    return other_to_one

def lt(one, other):
	return one < other

def gt(one, other):
	return one > other

def bdom(problem, one, other):
    """
    Return if one dominates two
    """
    dominates = False    
    for i in xrange(len(one)):
    	op = gt
    	if problem.objective_type[i] == objectives.DO_MINIMIZE: op = lt
        if op(one[i], other[i]) :
            dominates = True
    	elif one[i] == other[i]:
			continue
    	else:
			return False
    return dominates
