#!/usr/bin/python

from __future__ import division
import sys
import random
import math

sys.dont_write_bytecode=True

MIN = None
MAX = None
KMAX = 1000
EPSILON = 1.01

def shafer(x):
    ''' f1() + f2() '''
    return (x*x) + (x-2)*(x-2)

def get_s():
    ''' generates a random s in gicen range '''
    return random.uniform(-10000.0, 10000.0)

def find_min_max():
    ''' finds minimum and maximum value of given function '''
    global MIN, MAX
    min = float('inf')
    max = float('-inf')
    for i in range(100):
        x = get_s()
        s = shafer(x)
        if s<min :
            min = s
        if s>max :
            max = s
    MIN = min
    MAX = max
    #print "min: ", MIN, "max: ", MAX

'''
s := s0; e := E(s)                  // Initial state, energy.
sb := s; eb := e                    // Initial "best" solution
k := 0                              // Energy evaluation count.
WHILE k < kmax and e > emax         // While time remains & not good enough:
  sn := neighbor(s)                 //   Pick some neighbor.
  en := E(sn)                       //   Compute its energy.
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

def E(s):
    ''' calculates noramlized energy/value of shafer '''
    e = shafer(s)
    return ((e - MIN) / (MAX - MIN))

def normalize_e(e):
    ''' normalizes wrt our MIN and MAX '''
    return ((e - MIN) / (MAX - MIN))

def neighor(s):
    ''' finds a neighbour point within 10 units '''
    return random.uniform(s*0.99, s*1.01)
    # return (s + random.uniform(-10, 10))

def P(e, en, k):
    ''' calculates probability for random jump in simulated annealing '''
    if not k:
        return 1.0
    return math.exp((e-en)/k)   

def simulate():
    ''' simulated annealing implementation for minimizing a function '''
    s = get_s()
    e = E(s)
    emin = normalize_e(MIN + EPSILON)
    sb = s
    eb = e
    k = 0
    # print k, KMAX, e, emin, s
    print "%04d" % k, round(e, 1), " ",
    while k < KMAX and e > emin:
        sn = neighor(s)
        en = E(sn)
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
    return sb

def simulate_max():
    ''' simulated annealing implementation for maximizing a function '''
    s = get_s()
    e = E(s)
    emax = normalize_e(MAX - EPSILON)
    sb = s
    eb = e
    k = 0
    # print k, KMAX, e, emax, s
    print "\n", k, round(e, 1), " "
    while k < KMAX and e < emax:
        sn = neighor(s)
        en = E(sn)
        if en > eb:
            sb = sn
            eb = en
            sys.stdout.write("!")

        # print "k/kmax", k/KMAX, k, KMAX
        if en > e:
            s = sn
            e = en
            sys.stdout.write("+")
        elif P(en, e, k/KMAX) < random.random():
            s = sn
            e = en
            sys.stdout.write("?")
        sys.stdout.write(".")
        
        k+=1
        if k%25 == 0:
            print "\n", k, round(e, 1), " "
    # print "\n", k, KMAX, e, emax
    return sb

def main():
    random.seed(1)
    find_min_max()
    sb = simulate()
    # print "\n", sb

if __name__=='__main__':
    main()

