#!/usr/bin/python

from __future__ import division
import sys
import random
import math
import utils

MIN = None
MAX = None
KMAX = 1000
EPSILON = .01

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
    return ((e - MIN) / (MAX - MIN))

def normalize_e(e):
    ''' normalizes wrt our MIN and MAX '''
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

def simulate(problem, min, max):
    ''' simulated annealing implementation for minimizing a function '''
    s = problem.generate_one()
    e = E(problem, s)
    emin = normalize_e(MIN + EPSILON)
    sb = s
    eb = e
    k = 0
    # print k, KMAX, e, emin, s
    print "%04d" % k, round(e, 1), " ",
    while k < KMAX and e > emin:
        sn = neighor(problem, s)
        en = E(problem, sn)
        if en < eb:
            sb = sn
            eb = en
            sys.stdout.write("!")

        # print "k/kmax", k/KMAX, k, KMAX
        if en < e:
            s = sn
            e = en
            sys.stdout.write("+")
        elif P(e, en, k/KMAX) < random.random():
            s = sn
            e = en
            sys.stdout.write("?")
        sys.stdout.write(".")
        
        k+=1
        if k%25 == 0:
            print "\n", "%04d" % k, round(e, 6), " ",
    #print "\n", k, KMAX, e, emin
    return sb, eb

def sa(problem):
    global MIN, MAX
    print "##########################"
    print "Simulated Annealing for", problem.__class__.__name__
    random.seed(1)
    MIN, MAX = utils.find_min_max(problem)
    sb, eb = simulate(problem, min, max)
    print "\nBest solution", [round(x, 6) for x in sb]
    print "pre calculated minimum and maximum are", round(MIN, 6), "and", round(MAX, 6)
    print "Best normalized score", round(eb, 6)


