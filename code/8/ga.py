
# All the imports
from __future__ import print_function, division
from math import *
import random
import sys
import matplotlib.pyplot as plt

# Few Utility functions
def say(*lst):
    """
    Print whithout going to new line
    """
    print(*lst, end="")
    sys.stdout.flush()

def random_value(low, high, decimals=2):
    """
    Generate a random number between low and high. 
    decimals incidicate number of decimal places
    """
    return round(random.uniform(low, high),decimals)

def gt(a, b): return a > b

def lt(a, b): return a < b

def shuffle(lst):
    """
    Shuffle a list
    """
    random.shuffle(lst)
    return lst

def crossover(mom, dad):
    n = len(mom.decisions)    
    return Point(mom.decisions[:n//2] + dad.decisions[n//2:])

def mutate(problem, point, mutation_rate=0.01):
    for i, decision in enumerate(problem.decisions):
        if random.random() < mutation_rate:
            point.decisions[i] = random_value(decision.low, decision.high)
    return point

def fast_non_dom_sort(problem, population):
    class FrontierPt(object):
        id = 0
        def __init__(self, s = [], n = 0, rank = 0, decisions = []):
            FrontierPt.id += 1
            self.s = s
            self.n = n
            self.rank = rank
            self.decisions = decisions
            self.id = FrontierPt.id

    mypop = [FrontierPt(decisions = X) for X in population]
    frontiers = [[]]
    for p in mypop:
        p_obj = problem.get_objectives(p)
        for q in mypop:
            if q.id == p.id: continue  # bottleneck
            q_obj = problem.get_objectives(q)
            if utils.bdom(p_obj, q_obj):
                p.s.append(q)
            elif utils.bdom(q_obj, p_obj):
                np += 1
        if not np:
            prank = 1
            frontiers[0].append(p)
        i = 0
        while not frontiers[i]:
            Q = []
            for p in frontiers[i]:
                for q in p.s:
                    q.n -= 1
                    if not nq:
                        q.rank = i + 1
                        Q.append(q)
            i += 1
            frontiers.append(Q)
    return [[frontier_pt.decisions for frontier_pt in frontier] for frontier in frontiers]

def cuboid_sort_select(problem, to_select, frontier):
    class CSortPt(object):
        def __init__(self, decisions, objectives):
            self.decisions = decisions
            self.objectives = objectives
            self.ip = 0.0
    myfrontier = [CSortPt(X, problem.get_objectives(X)) for X in frontier]
    for i in range(len(objectives)):
        myfrontier = sorted(myfrontier, key = lambda Pt: Pt.objectives[i])
        lo = myfrontier[0].objectives[i]
        hi = myfrontier[-1].objectives[i]
        range = hi - lo
        for j in range(len(myfrontier)):
            ip = 0.0
            if j-1 > 0: 
                ip += myfrontier[j].objectives[i] - myfrontier[j-1].objectives[i]
            if j+1 < len(myfrontier): 
                ip += myfrontier[j+1].objectives[i] - myfrontier[j].objectives[i]
            ip = ip / range
            myfrontier[j].ip += ip
    myfrontier = sorted(myfrontier, key = lambda X: X.ip, reverse = True)[:to_select]
    return [X.decisions for X in myfrontier]

def select(problem, population, retain_size):
    frontiers = fast_non_dom_sort(population)
    i = 0
    new_pop = []
    while len(new_pop) + len(frontiers[i]) <= retain_size:
        new_pop += frontiers[i]
        i+=1
    if len(new_pop) == retain_size:
        return new_pop
    # do additional pruning in frontier i
    to_select = retain_size - len(new_pop)
    new_pop += cuboid_sort_select(problem,to_select, frontiers[i])
    assert(len(new_pop) == retain_size)
    return new_pop

def ga(problem, pop_size = 100, gens = 250):
    population = [problem.generate_one() for _ in range(pop_size)]
    initial_population = population[:]
    gen = 0 
    while gen < gens:
        say(".")
        children = []
        for _ in range(pop_size):
            # can improbe choice by touranament selection
            mom = random.choice(population)
            dad = random.choice(population)
            while (mom == dad):
                dad = random.choice(population)
            child = mutate(problem, crossover(mom, dad))
            if problem.is_valid(child) and child not in population+children:
                children.append(child)
        population += children
        population = select(problem, population, pop_size)
        gen += 1
    print("")
    return initial_population, population

def plot_pareto(initial, final):
    initial_objs = [point.objectives for point in initial]
    final_objs = [point.objectives for point in final]
    initial_x = [i[0] for i in initial_objs]
    initial_y = [i[1] for i in initial_objs]
    final_x = [i[0] for i in final_objs]
    final_y = [i[1] for i in final_objs]
    plt.scatter(initial_x, initial_y, color='b', marker='+', label='initial')
    plt.scatter(final_x, final_y, color='r', marker='o', label='final')
    plt.title("Scatter Plot between initial and final population of GA")
    plt.ylabel("Total Surface Area(T)")
    plt.xlabel("Curved Surface Area(S)")
    plt.legend(loc=9, bbox_to_anchor=(0.5, -0.175), ncol=2)
    plt.show()

initial, final = ga()
plot_pareto(initial, final)
