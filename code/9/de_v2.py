#!/usr/bin/python

from __future__ import division
import random
import sys
import objectives
import copy
import stats

# de/rand/1
MIN=None
MAX=None

dtsz_obj_map = {'DTSZ5': objectives.DTSZ5, 'DTSZ7': objectives.DTSZ7, 'DTSZ1': objectives.DTSZ1, 'DTSZ3': objectives.DTSZ3}

file_handle = None
def n(max):
  return int(random.uniform(0,max))

class Thing():
  id = 0
  def __init__(self, **entries): 
    self.id = Thing.id = Thing.id + 1
    self.__dict__.update(entries)

def my_de(max  = 10000,  # number of repeats 
       np      = 10,  # number of candidates
       f       = 0.75, # extrapolate amount
       cf      = 0.3,  # prob of cross-over 
       epsilon = 0.0001,
       problem = None
     ):
  frontier = [objectives.GAPoint(problem.generate_one(), problem) for _ in range(np)] 
  base_pop = frontier[:]
  last_frontier = frontier[:]
  last_total = 1.0 * np
  lives = 2
  for k in range(max):
    print >> file_handle, "DE: Gen", k
    file_handle.flush()
    total,n = update(f,cf,frontier,problem)
    #print (sum([score(problem, x ) for x in frontier])/len(frontier)), total/n, MIN, MAX
    if abs(last_total/n - total/n) <= epsilon: lives -= 1
    else: lives = 2
    if not lives: break
    last_frontier = frontier[:]
    last_total = total
    #if total/n < epsilon: 
    #  break
  return base_pop, frontier

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
   return this > that  # Since in this case we have to maximize both the objectives

def trim(x,d,problem)  : # trim to legal range
  return max(problem.decisions[d].low, min(x, problem.decisions[d].high))

def score(problem, x):
    s = problem.normalise_obj(x.evaluate())
    return s

def extrapolate(frontier,one,f,cf, problem):
  out = objectives.GAPoint(one.decisions, problem)
  two,three,four = threeOthers(frontier,one)
  changed = False  
  for d in range(len(problem.decisions)):
    #x,y,z = two[d], three[d], four[d]
    if random.random() < cf:
      changed = True
      # ignore f, just pick a random index
      #new     = x + f*(y - z)
      #out[d]  = trim(new,d,problem) # keep in range
      #TODO make an effort not to selct the same value
      out.decisions[d] = problem.decisions[d].any()
  if not changed:
    d      = random.randint(0, len(problem.decisions)-1) 
    out.decisions[d] = two.decisions[d]
  return out

#Returns three different things that are not 'avoid'.
def threeOthers(lst, avoid):
  def oneOther():
    x = avoid
    while x.id in seen: 
      x = a(lst)
    seen.append( x.id )
    return x
  # -----------------------
  seen = [ avoid.id ]
  this = oneOther()
  that = oneOther()
  theOtherThing = oneOther()
  return this, that, theOtherThing

def a(lst) :
  return lst[n(len(lst))]

def de(gaproblem):
    global MIN, MAX
    MIN, MAX = gaproblem.find_min_max()
    print >> file_handle, "DE: min max found"
    file_handle.flush()
    init, final = my_de(problem = gaproblem)
    for pt in final: print >> file_handle, pt.decisions, ":", pt.evaluate()
    file_handle.close()
    #return sols  # returning a pareto frontier of 30 points
    #return my_de(problem = problem)

if __name__ == "__main__":
	argv = sys.argv
	dtszobj = dtsz_obj_map[argv[1]](int(argv[2]),int(argv[3]))
	filename = argv[1] + "_" + argv[2] + "_" + argv[3] + ".log"
	file_handle = open(filename, "w")
	de(objectives.GAProblem(dtszobj))

#de(objectives.GAProblem(objectives.DTSZ7(10,2)))
