#!/usr/bin/python

from __future__ import division
import random
import sys
import utils
import objectives
import copy
import sa, mws, de
import stats

# Run each algo 20 times
# We'll get 20 pareto frontiers each
# Each point in pareto frontier corresponds to two objectives
# convert frontiers to objective values which will get us pareto frontier in obj space
# Convert frontiers into loss numbers
# So 20 loss numbers for each algo
# then do the comparison

optimizers = [sa.sa_frontier_gen, mws.mws_frontier_gen, de.de]
opt_names = ["sa", "mws", "de"]
losses = {'mws': [209393.0, 173745.0, 170771.0, 176247.0, 181512.0, 153744.0, 161202.0, 171947.0, 210590.0, 167728.0, 148798.0, 196903.0, 144528.0, 240014.0, 185198.0, 175432.0, 187342.0, 206929.0, 131043.0, 138169.0], 'sa': [189730.0, 148717.0, 200948.0, 173639.0, 121437.0, 211964.0, 157286.0, 101812.0, 175932.0, 181762.0, 141423.0, 133650.0, 161947.0, 151125.0, 150785.0, 112751.0, 106508.0, 110009.0, 200990.0, 162487.0], 'de': [198330.0, 212810.0, 219706.0, 192503.0, 168084.0, 202484.0, 214697.0, 191917.0, 215609.0, 161384.0, 243106.0, 175245.0, 141492.0, 176310.0, 192287.0, 183313.0, 280215.0, 305462.0, 211448.0, 175309.0]}

def run_20_times():
    global losses
    for i in range(len(optimizers)):
        losses[opt_names[i]] = []
        for j in range(20):
            print i, j
            problem = objectives.DTSZ7(10, 2)
            base, pareto = optimizers[i](problem)
            loss = sum ([ utils.cdom_loss(problem, base_one, pareto_one) for pareto_one in pareto 
                    for base_one in base ]) 
            print loss
            losses[opt_names[i]].append(loss)
    for k, v in losses:
        print k, v
    return losses

#def find_losses():

def collect_type1_stats():
    print "##### Medians ######"
    for name in opt_names:
        [mid1, mid2] = sorted(losses[name])[9:11]
        #print name, ":", (mid1 + mid2)/2
        print name, ":", stats.xtile(losses[name])

def collect_type2_stats():
    print "##### a12 ######"
    for i in range(len(opt_names)):
        for j in range(len(opt_names)):
            if i>=j: continue
            print "a12 test for", opt_names[i], "and", opt_names[j], stats.a12(losses[opt_names[i]], losses[opt_names[j]])


def collect_type3_stats():
    print "##### bootstrap ######"
    for i in range(len(opt_names)):
        for j in range(len(opt_names)):
            if i>=j: continue
            print "bootstrap test for", opt_names[i], "and", opt_names[j], stats.bootstrap(losses[opt_names[i]], losses[opt_names[j]])

def my_scottknott():
    print "##### scott-knott ######"
    data = []
    for name in opt_names:
        data.append([name] + losses[name])
    stats.rdivDemo(data)

collect_type1_stats();
collect_type2_stats();
collect_type3_stats();
my_scottknott();
