#!/usr/bin/python

'''
FOR i = 1 to max-tries DO
  solution = random assignment
  FOR j =1 to max-changes DO
    IF  score(solution) > threshold
        THEN  RETURN solution
    FI
    c = random part of solution 
    IF    p < random()
    THEN  change a random setting in c
    ELSE  change setting in c that maximizes score(solution) 
    FI
RETURN failure, best solution found
'''
from __future__ import division
import random
import sys

MAX_RETRIES=20
MAX_CHANGES=30
MIN=None
MAX=None
THRESHOLD=0.00000001

def r(): return random.random()

class Decision(object):
    def __init__(self, name, low, high):
        self.name = name
        self.low = low
        self.high = high

    def any(self):
        return self.low + r()*(self.high - self.low)

class Problem(object):
    """
    Class representing the problem.
    """
    def __init__(self):
        self.decisions = [Decision('x1', 0, 10), Decision('x2', 0, 10),
                          Decision("x3", 1, 5), Decision("x4", 0, 6), 
                          Decision("x5", 1, 5), Decision("x6", 0, 10)]
   
    @staticmethod
    def is_valid(sol):
        [x1, x2, x3, x4, x5, x6] = sol
        g1 = x1 + x2 - 2
        g2 = 6 - x1 - x2
        g3 = 2 - x2 + x1
        g4 = 2 - x1 + 3*x2
        g5 = 4 - (x3-3)**2 - x4
        g6 = (x5-3)**3 + x6 - 4
        if g1>=0 and g2>=0 and g3>=0 and g4>=0 and g5>=0 and g6>=0:
            return True
        return False
    
    def generate_one(self):
        max_ret = 10000
        i = 0
        while(i<max_ret):
            sol = [self.decisions[i].any() for i in range(len(self.decisions))]
            if Problem.is_valid(sol):
                return sol
            i+=1
        print "Error generate_one(): couldnt generate solution"
        return None
    
    def mutate_one(self, sol, pos):
        max_ret = 100000
        i = 0
        new_sol = sol[:]
        while(i<max_ret):
            new_sol[pos] = self.decisions[pos].any()  
            if Problem.is_valid(new_sol):
                return new_sol
            i+=1
        #print "Error mutate_one(): couldnt generate solution for pos", pos
        return sol
    
    def local_search(self, sol, pos):
        # Take steps of k/10
        lo = self.decisions[pos].low
        hi = self.decisions[pos].high
        step = (hi - lo)/10;
        obj = norm_objective(sol)
        sol[pos] = lo
        obj = norm_objective(sol)
        best_sol_pos = sol[pos]
        for i in range(10):
            sol[pos] += step
            if not not Problem.is_valid(sol):
                continue
            new_obj = max(obj, norm_objective(sol))
            if new_obj > obj:
                best_sol_pos = sol[pos]
                obj = new_obj
        sol[pos] = best_sol_pos
        return sol

def objective(decisions):
    '''Calculates the value of osckyza function'''
    [x1, x2, x3, x4, x5, x6] = decisions
    f1 = -25*((x1 - 2)**2) + (x2-2)**2 + ((x3-1)**2)*((x4-4)**2) + (x5-1)**2
    f2 = x1**2 + x2**2 + x3**2 + x4**2 + x5**2 + x6**2
    return f1+f2

def norm_objective(decisions):
    ''' normalizes the objective, based on precalculated approximate bounds of function''' 
    ''' Note that it need not return values in the interval [0,1] since bounds are only approcimate'''

    obj = objective(decisions)
    return (obj - MIN)/(MAX - MIN)


def mwsfiddle(old, problem):
    '''Probabilistically either modifies a random decision or does local search'''
    # Pick a decisions
    new = old[:]  # copy
    pos = random.randint(0, len(old)-1)
    # check probability
    if r() > 0.5:
        # mutate new[pos] until you obtain a valid mutation satisfying all constraints
        return problem.mutate_one(new, pos)
    return problem.local_search(new, pos)

def find_min_max(problem):
    ''' finds minimum and maximum value of given function '''
    global MIN, MAX
    min = float('inf')
    max = float('-inf')
    for i in range(100000):
        sol = problem.generate_one()
        obj = objective(sol)
        if obj<min :
            min = obj
        if obj>max :
            max = obj
    MIN = min
    MAX = max

def mws():
    '''Runs MaxWalkSat algorithm'''
    random.seed(31)
    problem = Problem()
    find_min_max(problem)
    best_score = 0.0
    best_sol = None
    for i in range(MAX_RETRIES):
        solution = problem.generate_one()
        prev_score = 0.0
        print "iteration", i, ':',
        for j in range(MAX_CHANGES):
            score = norm_objective(solution)
           #if 1 - score <= THRESHOLD:
           #    print 'solution found', solution
           #    return solution
            if score > best_score:
                sys.stdout.write("!")
                best_score = score
                best_sol = solution[:]
            if score > prev_score:
                sys.stdout.write("+")
            else:
                sys.stdout.write(".")

            prev_score = score
            solution = mwsfiddle(solution, problem) 
        sys.stdout.write(" " + str(best_score))
        print ''
    print "Number of retries", MAX_RETRIES
    print "Number of iterations in each retry", MAX_CHANGES
    print "Best solution", best_sol
    print "pre calculated minimum and maximum are", MIN, "and", MAX
    print "Best score", best_score

mws()
