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
import utils
import objectives
import copy

MAX_RETRIES=100
MAX_CHANGES=100
MIN=None
MAX=None
THRESHOLD=0.00000001
FRONTIER_SIZE = 30

def mutate_one(problem, sol, pos):
    max_ret = 100000
    i = 0
    new_sol = sol[:]
    while(i<max_ret):
        new_sol[pos] = problem.decisions[pos].any()  
        if problem.is_valid(new_sol):
            return new_sol
        i+=1
    #print "Error mutate_one(): couldnt generate solution for pos", pos
    return sol
    
def local_search(problem, sol, pos):
    # Take steps of k/10
    lo = problem.decisions[pos].low
    hi = problem.decisions[pos].high
    step = (hi - lo)/10;
    obj = norm_objective(problem, sol)
    sol[pos] = lo
    obj = norm_objective(problem, sol)
    best_sol_pos = sol[pos]
    for i in range(10):
        sol[pos] += step
        if not problem.is_valid(sol):
            continue
        new_obj = min(obj, norm_objective(problem, sol))
        if new_obj < obj:
            best_sol_pos = sol[pos]
            obj = new_obj
    sol[pos] = best_sol_pos
    return sol

def norm_objective(problem, decisions):
    ''' normalizes the objective, based on precalculated approximate bounds of function''' 
    global MIN, MAX
    obj = problem.evaluate(decisions)
    if obj < MIN: MIN = obj
    if obj > MAX: MAX = obj
    return (obj - MIN)/(MAX - MIN)


def mwsfiddle(old, problem):
    '''Probabilistically either modifies a random decision or does local search'''
    # Pick a decisions
    new = old[:]  # copy
    pos = random.randint(0, len(old)-1)
    # check probability
    if utils.r() > 0.5:
        # mutate new[pos] until you obtain a valid mutation satisfying all constraints
        return mutate_one(problem, new, pos)
    return local_search(problem, new, pos)

def mws(problem, base_pop):
    '''Runs MaxWalkSat algorithm'''
    best_score = 1.0
    best_sol = None
    last_best_sol = None
    lives = 5
    init = False
    for i in range(MAX_RETRIES):
        solution = problem.generate_one()
        if not init:
			base_pop.append(solution)
			init = True
        for j in range(MAX_CHANGES):
            score = norm_objective(problem, solution)
            if score <= best_score:
                best_score = score
                best_sol = solution[:]
            solution = mwsfiddle(solution, problem) 
        if last_best_sol == best_sol:
            if not lives: break;
            lives -= 1
        else:
            lives = 5
        last_best_sol = copy.deepcopy(best_sol)
    #print "Best solution", [round(x,6) for x in best_sol], round(problem.evaluate(best_sol), 6), i
    #print "Best solution", round(problem.evaluate(best_sol), 6), i
    #print "pre calculated minimum and maximum are", round(MIN, 6), "and", round(MAX, 6)
    return best_sol

def mws_frontier_gen(problem):
    #print "##########################"
    #print "MaxWalkSat for", problem.__class__.__name__
    global MIN, MAX
    #random.seed(1)
    MIN, MAX = utils.find_min_max(problem)
    frontier = []
    base_pop = []
    for i in range(FRONTIER_SIZE):
        frontier.append(mws(problem, base_pop))
    return [problem.get_objectives(X) for X in base_pop], [problem.get_objectives(X) for X in frontier]

#mws_frontier_gen(objectives.DTSZ7(10, 2))
