'''
iteration 3 from 2.
It is different because:
Take one square. If there is one predator there in the second iteration we iterate over the eating sequence by the amount of prey there. If there is multiple predators there we still iterate over the eating sequence by the number of prey.
To be closer to Lotka Volterra, we should be iterating over the eating sequence by numb of prey * numb of predators. To account for preys dying from this, we will loop through the number of predators and after each predator, the number of prey is docked by the amount that got killed by that predator.
So say 3 pred 3 prey in a box it used to be 1 of those pred would try to eat all 3.
Now it is 1 pred will try to eat all 3, say he eats 1, then the next pred will try for 2 say he gets none then 3rd pred tries for 2 again.
'''
import matplotlib.pyplot as plt

from AnimalParameters import AnimalParameters
from GraphOptions import GraphOptions
from Experimenter import Experimenter
from ExperimentData import ExperimentData
from ExperimentOptions import ExperimentOptions
from Analyser import Analyser
from EnAData import EnAData, FiledEnAData
from DisplayAnalysis import DisplayAnalysis
from DisplayTogether import DisplayTogether
from Recipes import Recipes

# Parameters
a = 0.8 # Probability that if a prey gets paired with a predator, it will die
b = 0.2 # Probability that if a predator gets paired with a prey, it will reproduce
c = 0.2 # Probability that a prey will reproduce
d = 0.1 # Probability of death for a predator

# Graph options
col_num = row_num = 40 # row_num by column_num grid
initial_num_predators = 300
initial_num_prey = 600

# Experiment options
num_turns = 200 # Number of turns
experiment_name = 'same_ic'

experiment_folder = 'output'

parameters = AnimalParameters(a, b, c, d)
options = GraphOptions(col_num, row_num, initial_num_predators, initial_num_prey)
exops = ExperimentOptions(experiment_name, num_turns)

if __name__ == '__main__':
    cook = Recipes()
    displayer = cook.run_and_display(
        graph_options = options,
        animal_parameters = parameters,
        experiment_options = exops
    )
    displayer.save_point_map_video()

