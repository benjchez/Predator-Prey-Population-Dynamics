'''
iteration 2 (it2) refactored AGAIN (may have slightly different functionality but ethos is the same).
'''
from AnimalParameters import AnimalParameters
from GraphOptions import GraphOptions
from Experimenter import Experimenter
from ExperimentOptions import ExperimentOptions
from Analyser import Analyser

# Parameters
a = 0.8 # Probability that if a prey gets paired with a predator, it will die
b = 0.1 # Probability that if a predator gets paired with a prey, it will reproduce
c = 0.01 # Probability that a prey will reproduce
d = 0 # Probability of death for a predator

# Graph options
col_num = row_num = 10 # row_num by column_num grid
initial_num_predators = 60
initial_num_prey = 100

# Experiment options
num_turns = 3 # Number of turns
experiment_name = 'test1'

parameters = AnimalParameters(a, b, c, d)
options = GraphOptions(col_num, row_num, initial_num_predators, initial_num_prey)
exops = ExperimentOptions(experiment_name, num_turns)

if __name__ == '__main__':
    experiment = Experimenter(options, parameters, exops)
    analyse = Analyser('output/test', 'test')
    analyse.write_pm()
    # experiment.out_to_files()
