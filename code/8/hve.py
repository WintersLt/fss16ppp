from __future__ import print_function, unicode_literals
from __future__ import absolute_import, division
from random import uniform
import objectives
import utils

"is the peddle inside the hyper volume"
def inbox(problem, pebble,frontier):
    for candidate in frontier:
        if utils.bdom(problem, candidate,pebble):
            return True
    return False


"estimate hyper volumn of frontier"
def hve(problem, frontier,sample=100000):
    count=0
    frontier = [problem.get_objectives(X) for X in frontier]
    for i in xrange(sample):
        pebble=problem.get_objectives(problem.generate_one())
        if inbox(problem,pebble,frontier):
            count=count+1
    return count/(sample)
