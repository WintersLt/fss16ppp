from __future__ import division
import random
import sys
import copy
import stats

objective_types = ['DTSZ1', 'DTSZ3', 'DTSZ5', 'DTSZ7']
num_decisions = [10, 20, 40]
num_objectives = [2, 4, 6, 8]

def extract():
    for objective in objective_types:
        for num_decision in num_decisions:
            for num_objective in num_objectives:
                filename = objective + "_" + str(num_decision) + "_" + str(num_objective) + ".log"
                max_hve = 0.0
                max_param = ""
                print "searching file", filename
                with open(filename, "r") as f:
                    for line in f:
                        if line[0] != '[': continue
                        [param, hve] = line.split(" : ")
                        #param = param[1:-1].split(",")
                        if hve > max_hve: 
                            max_hve = hve
                            max_param = param
                print filename[:-4], ":", max_param


extract() 
