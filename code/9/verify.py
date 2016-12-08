import objectives
import utils
import random
import sys
import time
import subprocess, os

#objective_types = ['DTSZ1', 'DTSZ3', 'DTSZ5', 'DTSZ7']
objective_types = ['DTSZ1']#, 'DTSZ3', 'DTSZ5', 'DTSZ7']
#num_decisions = [10, 20, 40]
num_decisions = [10]#, 20, 40]
#num_objectives = [2, 4, 6, 8]
num_objectives = [2]#, 4, 6, 8]
data_map = {'DTSZ1_10_2' : [0.15, 'single_pt', 'gacdom', 40, 45]}
def run_20():
    pids = set()
    for objective in objective_types:
        for num_decision in num_decisions:
            for num_objective in num_objectives:
                args = ["/usr/bin/python", "./ga.py", objective, str(num_decision), str(num_objective)]
                key ="_".join([objective, str(num_decision), str(num_objective)])

                paramlst = data_map[key]
                paramlst = [str(x) for x in paramlst]
                args += paramlst

                p = subprocess.Popen(args)
                pids.add(p.pid)
    while pids:
        pid, retval = os.wait()
        print pid, " finished execution"
        pids.remove(pid)


run_20()
