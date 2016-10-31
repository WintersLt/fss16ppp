#!/usr/bin/python

from __future__ import division
import sys
import random
import math

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

def find_min_max(problem):
    ''' finds minimum and maximum value of given function '''
    low = float('inf')
    high = float('-inf')
    for i in range(100):
        sol = generate_one(problem)
        s = problem.evaluate(sol)
        if s<low :
            low = s
        if s>high :
            high = s
    return low, high

def r(): 
    return random.random()
