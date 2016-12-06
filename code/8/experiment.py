import ga
import objectives
import utils
import random

num_repeats = 20
types = [utils.bdom, utils.cdom]
objective_types = [objectives.DTSZ1, objectives.DTSZ3, objectives.DTSZ5, objectives.DTSZ7]
num_decisions = [10, 20, 40]
num_objectives = [2, 4, 6, 8]

def run_experiments():
    for objective in objective_types:
        for num_decision in num_decisions:
            for num_objective in num_objectives:
                problem = objective(num_decision,num_objective)
                problem.find_min_max()
                for type in types:
                    print objective.__name__ + ".%d.%d" % (num_decision, num_objective) + "." + type.__name__, "= [",
                    for repeat_ct in range(num_repeats):
                        random.seed(1131 + repeat_ct*2 - 1)
                        print ga.ga(problem = problem, better = type), ",",
                    print "]"


run_experiments()


