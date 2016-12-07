import objectives
import utils
import random
import sys
import time
import subprocess, os

num_repeats = 20
objective_types = [objectives.DTSZ1, objectives.DTSZ3, objectives.DTSZ5, objectives.DTSZ7]
num_decisions = [10, 20, 40]
num_objectives = [2, 4, 6, 8]

#hashmap from problem type dec obj and seed to initial hve
dp_init_hve = {}

def run_experiments():
    pids = set()
    for objective in objective_types:
        for num_decision in num_decisions:
            for num_objective in num_objectives:
                #dtlz_prob = objective(num_decision, num_objective)
                #ga_prob = objectives.GAProblem(dtlz_prob)
                args = ["/usr/bin/python", "./de_v2.py",objective.__name__, str(num_decision), str(num_objective)]
                p = subprocess.Popen(args)
                pids.add(p.pid)
                return
    while pids:
        pid, retval = os.wait()
        print pid, " finished execution"
        pids.remove(pid)

run_experiments()

#               for type in types:
#                   key = objective.__name__ + ".%d.%d" % (num_decision, num_objective) + "."
#                   print objective.__name__ + ".%d.%d" % (num_decision, num_objective) + "." + type.__name__, "= [",
#                   skip_repeats = False
#                   for repeat_ct in range(num_repeats):
#                       if skip_repeats: continue
#                       seed = 1131 + repeat_ct*2 - 1
#                       random.seed(seed)
#                       tmp_key = str(key) + str(seed)
#                       start = time.time()
#                       print ga.ga(problem = problem, better = type, dp_init_hve=dp_init_hve, key=tmp_key), ",",
#                       if time.time() - start > 120.0: skip_repeats = True
#                       sys.stdout.flush()
#                   print "]"
#                   sys.stdout.flush()


