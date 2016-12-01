#!/usr/bin/python

from __future__ import division
import sys
import random
import math
import utils
import objectives
import copy

MIN = None
MAX = None
KMAX = 10000
EPSILON = .01
EVALS_PER_GEN = 100
FRONTIER_SIZE = 30

'''
s := s0; e := E(s)                  // Initial state, energy.
sb := s; eb := e                    // Initial "best" solution
k := 0                              // Energy evaluation count.
WHILE k < kmax and e > emax         // While time remains & not good enough:
  sn := neighbor(s)                 // Pick some neighbor.
  en := E(sn)                       // Compute its energy.
  IF    en < eb                     //   Is this a new best?
  THEN  sb := sn; eb := en          //     Yes, save it.
        print "!"
  FI
  IF    en < e                      // Should we jump to better?
  THEN  s := sn; e := en            //    Yes!
        print "+"                        
  FI
  ELSE IF P(e, en, k/kmax) < rand() // Should we jump to worse?
  THEN  s := sn; e := en            //    Yes, change state.
        print "?"
  FI
  print "."
  k := k + 1                        //   One more evaluation done    
  if k % 50 == 0: print "\n",sb
RETURN sb  
'''

def E(problem, s):
    ''' calculates noramlized energy/value of shafer '''
    e = problem.evaluate(s)
    return normalize_e(e)

def normalize_e(e):
    ''' normalizes wrt our MIN and MAX '''
    global MIN, MAX
    if (e<MIN): MIN = e
    if (e>MAX): MAX = e 
    return ((e - MIN) / (MAX - MIN))

def neighor(problem, solution):
    ''' finds a neighbor point within 10 units '''
    new_sol = []
    for x, decision in zip(solution, problem.decisions):
        step = (decision.high - decision.low)/100.0
        x = random.uniform(max(x-step, decision.low), min(x+step, decision.high))
        new_sol += [x]
    return new_sol

def P(e, en, k):
    ''' calculates probability for random jump in simulated annealing '''
    if not k:
        return 1.0
    return math.exp((e-en)/k)   

def simulate(problem, min, max, base_pop):
    ''' simulated annealing implementation for minimizing a function '''
    s = problem.generate_one()
    base_pop.append(s)
    e = E(problem, s)
    emin = normalize_e(MIN + EPSILON)
    sb = s
    eb = e
    k = 0
    el = None; sl = None
    lives = 5
    while k < KMAX: #and e > emin:
        if k%EVALS_PER_GEN == 0:
            if(sl == sb):
                if not lives:
                    break
                lives -= 1
            else:
                lives = 5
            sl = copy.deepcopy(sb)
            el = eb
        sn = neighor(problem, s)
        en = E(problem, sn)
        if en <= eb:
            sb = copy.deepcopy(sn)
            eb = en

        if en < e:
            s = sn
            e = en
        elif P(e, en, k/KMAX) < random.random():
            s = sn
            e = en
        
        k+=1
    #print "generations :", k/100
    return sb, eb

def sa_frontier_gen(problem):
    global MIN, MAX
    #print "##########################"
    #print "Simulated Annealing for", problem.__class__.__name__
    #random.seed(1)
    frontier = []
    # Note that putting find_min_max put of loop gives better results
    # because find_min_max more often than not return poor limit and our
    # sa is guided in the wrong direction initially
    MIN, MAX = utils.find_min_max(problem)
    base_pop = []
    for i in range(FRONTIER_SIZE):
        sb, eb = simulate(problem, min, max, base_pop)
        frontier.append(sb)
        #print "\nBest solution", [round(x, 6) for x in sb]
        #print "pre calculated minimum and maximum are", round(MIN, 6), "and", round(MAX, 6)
        #print "Best score", round(problem.evaluate(sb), 6)
    return [problem.get_objectives(X) for X in base_pop], [problem.get_objectives(X) for X in frontier]

#sa(objectives.DTSZ7(10, 2))
