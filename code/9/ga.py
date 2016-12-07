
# All the imports
from __future__ import print_function, division
from math import *
import random
import sys
import objectives
import utils
import matplotlib.pyplot as plt
import hve
import hve2
import time

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

def single_pt_crossover(mom, dad):
    n = len(mom)    
    return mom[:n//2] + dad[n//2:]

def two_pt_crossover(mom, dad):
    n = len(mom)    
    one = random.randint(1, n-1)
    two = random.randint(1, n-1)
    while one == two:
        two = random.randint(1, n-1)
    lesser = min(one, two)
    larger = max(one, two)
    return mom[0:lesser] + dad[lesser:larger] + mom[larger:]

def uniform_crossover(mom, dad):
    n = len(mom)
    out = []
    for i in range(n):
        if utils.r() < 0.5: out.append(mom[i])
        else: out.append(dad[i])
    return out

def crossover(mom, dad, crossover_type):
    if crossover_type == "single_pt": return single_pt_crossover(mom, dad)
    elif crossover_type == "two_pt": return two_pt_crossover(mom, dad)
    elif crossover_type == "uniform": return uniform_crossover(mom, dad)
    else: print("BUG BUG: Invalid crossover type")

def mutate(problem, point, mutation_rate=0.01):
    for i, decision in enumerate(problem.decisions):
        if random.random() < mutation_rate:
            point[i] = random_value(decision.low, decision.high)
    return point

def fast_non_dom_sort(problem, population, better=utils.bdom):
    class FrontierPt(object):
        id = 0
        def __init__(self, s = [], n = 0, rank = 0, decisions = []):
            FrontierPt.id += 1
            self.s = s[:]
            self.n = n
            self.rank = rank
            self.decisions = decisions[:]
            self.id = FrontierPt.id
    mypop = [FrontierPt(decisions = X) for X in population]
    frontiers = [[]]
    for p in mypop:
        p_obj = problem.get_objectives(p.decisions)
        for q in mypop:
            if q.id == p.id: continue
            q_obj = problem.get_objectives(q.decisions)
            if better(problem, p_obj, q_obj):
                p.s.append(q)
            elif better(problem, q_obj, p_obj):
                p.n += 1
        if not p.n:
            p.rank = 1
            frontiers[0].append(p)
    i = 0
    num_added = len(frontiers[0])
    num_needed = len(population)
    while len(frontiers[i]):
        Q = []
        for p in frontiers[i]:
            for q in p.s:
                q.n -= 1
                if not q.n:
                    q.rank = i + 2
                    Q.append(q)
        # if some frontier didn't directly give us next frontier, retry
        if not len(Q) and num_added < num_needed:
            continue
        i += 1
        frontiers.append(Q)
        num_added += len(Q)

    assert(sum([len(front) for front in frontiers]) == len(population))
    return [[frontier_pt.decisions for frontier_pt in frontier] for frontier in frontiers]

def cuboid_sort_select(problem, to_select, frontier):
    class CSortPt(object):
        def __init__(self, decisions, objectives):
            self.decisions = decisions
            self.objectives = objectives
            self.ip = 0.0
    myfrontier = [CSortPt(X, problem.get_objectives(X)) for X in frontier]
    for i in range(problem.num_obj):
        myfrontier = sorted(myfrontier, key = lambda Pt: Pt.objectives[i])
        lo = myfrontier[0].objectives[i]
        hi = myfrontier[-1].objectives[i]
        size = hi - lo or 1
        for j in range(len(myfrontier)):
            ip = 0.0
            if j-1 > 0: 
                ip += myfrontier[j].objectives[i] - myfrontier[j-1].objectives[i]
            if j+1 < len(myfrontier): 
                ip += myfrontier[j+1].objectives[i] - myfrontier[j].objectives[i]
            ip = ip / size
            myfrontier[j].ip += ip
    myfrontier = sorted(myfrontier, key = lambda X: X.ip, reverse = True)[:to_select]
    return [X.decisions for X in myfrontier]

def cdom_sort_select(problem, to_select, frontier):
    class CDOMSortPt(object):
        def __init__(self, decisions, objectives):
            self.decisions = decisions
            self.objectives = objectives
            self.num_pts_dominated = 0
    myfrontier = [CDOMSortPt(X, problem.get_objectives(X)) for X in frontier]
    # this is slow but number of points inside frontier wont be too many
    for i, one in enumerate(myfrontier):
        j = i+1
        while j < len(myfrontier):
            other = myfrontier[j]
            if utils.cdom(problem, one.objectives, other.objectives):
                one.num_pts_dominated += 1
            else:
                other.num_pts_dominated += 1
            j+=1

    myfrontier = sorted(myfrontier, key = lambda Pt: Pt.num_pts_dominated, 
            reverse=True)[:to_select]
    return [X.decisions for X in myfrontier]

def nsga2bdom_select(problem, population, retain_size):
    frontiers = fast_non_dom_sort(problem, population, utils.bdom)
    i = 0
    new_pop = []
    while len(new_pop) + len(frontiers[i]) < retain_size:
        new_pop += frontiers[i]
        i+=1
    if len(new_pop) == retain_size:
        return new_pop
    # do additional pruning in frontier i
    to_select = retain_size - len(new_pop)
    new_pop += cuboid_sort_select(problem,to_select, frontiers[i])
    
    assert(len(new_pop) == retain_size)
    return new_pop

def nsga2cdom_select(problem, population, retain_size):
    frontiers = fast_non_dom_sort(problem, population, utils.cdom)
    i = 0
    new_pop = []
    while len(new_pop) + len(frontiers[i]) < retain_size:
        new_pop += frontiers[i]
        i+=1
    if len(new_pop) == retain_size:
        return new_pop
    # do additional pruning in frontier i
    to_select = retain_size - len(new_pop)
    new_pop += cdom_sort_select(problem,to_select, frontiers[i])
    
    assert(len(new_pop) == retain_size)
    return new_pop

def gacdom_select(problem, population, retain_size):
    new_pop = cdom_sort_select(problem, retain_size, population)
   
    assert(len(new_pop) == retain_size)
    return new_pop

def select(problem, population, retain_size, select_type):
    if select_type == "nsga2bdom": return nsga2bdom_select(problem, population, retain_size)
    if select_type == "nsga2cdom": return nsga2cdom_select(problem, population, retain_size)
    if select_type == "gacdom": return gacdom_select(problem, population, retain_size)


def find_hve2(problem, population):
    start = time.time()
    solutions = [problem.get_objectives(X) for X in population]
    referencePoint = [1.5 * y for y in problem.obj_maxs]
    hv = hve2.InnerHyperVolume(referencePoint)
    ret = hv.compute(solutions)
    #print ("find_hve2: ", time.time() - start)
    return ret

def ga(problem, pop_size = 100, gens = 35, select_type="nsga2bdom",
        crossover_type = "single_pt", mutation_rate = 0.01,dp_init_hve={},key="none", 
		init_hve=None):
    random.seed(1) # in order to generate same output with same params
    problem.find_min_max()
    population = [problem.generate_one() for _ in range(pop_size)]
    initial_population = population[:]
    #hypervol = hve.hve(problem, population)
    if not init_hve:
        init_hve = find_hve2(problem, population)
    gen = 0 
    while gen < gens:
        #say(".")
        children = []
        for _ in range(pop_size):
            # can improbe choice by touranament selection
            mom = random.choice(population)
            dad = random.choice(population)
            while (mom == dad):
                dad = random.choice(population)
            child = mutate(problem, crossover(mom, dad, crossover_type), mutation_rate)
            if problem.is_valid(child) and child not in population+children:
                children.append(child)
        population += children
        population = select(problem, population, pop_size, select_type)
        gen += 1
    #print("")
    #hypervol = hve.hve(problem, population)
    hypervol = find_hve2(problem, population)
    #return initial_population, population
    return hypervol/init_hve, init_hve

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

#   random.seed(1131)
#   problem = objectives.DTSZ7(10,2)
#   problem.find_min_max()
#   print(ga(problem = problem, pop_size = 40, gens = 30, select_type = "nsga2bdom", 
#       mutation_rate = 0.1, crossover_type = "single_pt"))
#####initial, final = ga(problem = problem)
#####plot_pareto(initial, final)
