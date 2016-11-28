#!/usr/bin/python

from __future__ import division
import random
import sys
import utils
import objectives
import copy

# de/rand/1
MIN=None
MAX=None

def n(max):
  return int(random.uniform(0,max))

class Thing():
  id = 0
  def __init__(self, **entries): 
    self.id = Thing.id = Thing.id + 1
    self.__dict__.update(entries)

def my_de(max  = 5000,  # number of repeats 
       np      = 100,  # number of candidates
       f       = 0.75, # extrapolate amount
       cf      = 0.3,  # prob of cross-over 
       epsilon = 0.0001,
       problem = None
     ):
  frontier = [problem.generate_one() for _ in range(np)] 
  for k in range(max):
    total,n = update(f,cf,frontier,problem)
    if(k%2 == 0):
      print (sum([score(problem, x ) for x in frontier])/len(frontier)), total/n, MIN, MAX
    if total/n < epsilon: 
      break
  return frontier

def update(f,cf,frontier,problem, total=0.0, n=0):
  for i in range(len(frontier)):
    x = frontier[i]
    s   = score(problem,x)
    new = extrapolate(frontier,x,f,cf,problem)
    new_score = score(problem,new)
    if better(new_score, s):
      s = new_score
      frontier[i]  = new
    total += s
    n     += 1
  return total,n

def better(this,that):
   '''continuous or binary domination'''
   return this < that  # Since in this case we have to minimize both the objectives

def trim(x,d,problem)  : # trim to legal range
  return max(problem.decisions[d].low, min(x, problem.decisions[d].high))

def score(problem, x):
    global MIN, MAX
    s = problem.evaluate(x)
    if(s > MAX): MAX = s
    if(s < MIN): MIN = s
    return (s-MIN)/(MAX-MIN)

def extrapolate(frontier,one,f,cf, problem):
  out = copy.deepcopy(one)
  two,three,four = threeOthers(frontier,one)
  changed = False  
  for d in range(len(problem.decisions)):
    x,y,z = two[d], three[d], four[d]
    if utils.r() < cf:
      changed = True
      new     = x + f*(y - z)
      out[d]  = trim(new,d,problem) # keep in range
  if not changed:
    d      = random.randint(0, len(problem.decisions)-1) 
    out[d] = two[d]
  return out

#Returns three different things that are not 'avoid'.
def threeOthers(lst, avoid):
  def oneOther():
    x = avoid
    while x in seen: 
      x = a(lst)
    seen.append( x )
    return x
  # -----------------------
  seen = [ avoid ]
  this = oneOther()
  that = oneOther()
  theOtherThing = oneOther()
  return this, that, theOtherThing

def a(lst) :
  return lst[n(len(lst))]

def de(problem):
    global MIN, MAX
    MIN, MAX = utils.find_min_max(problem)
    sols = my_de(problem = problem)
    print(sum([score(problem, x ) for x in sols])/len(sols))
    for sol in sols:
        print sol

de(objectives.DTSZ7(10,2))
