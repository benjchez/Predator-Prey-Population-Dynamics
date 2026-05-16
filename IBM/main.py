'''
iteration 4 changes from 3 because:
Animals now have the same chance of staying still as moving. This will stop the away by two patterning of the prey on the grid.
'''
import matplotlib.pyplot as plt

from AnimalParameters import AnimalParameters
from GridOptions import GridOptions
from Experimenter import Experimenter
from ExperimentData import ExperimentData
from ExperimentOptions import ExperimentOptions
from Analyser import Analyser
from EnAData import EnAData, FiledEnAData
from DisplayAnalysis import DisplayAnalysis
from DisplayTogether import DisplayTogether
from Recipes import Recipes
from utils import resolve_seed

# Parameters
a = 0.3 # Probability that if a prey gets paired with a predator, it will die
b = 0.05 # Probability that if a predator gets paired with a prey, it will reproduce
c = 0.02 # Probability that a prey will reproduce
d = 0.005 # Probability of death for a predator

# Graph options
col_num = row_num = 15 # row_num by column_num grid
initial_num_predators = 10
initial_num_prey = 30

# Experiment options
num_turns = 500 # Number of turns
data_folder = 'output'
experiment_name = 'low-death'

experiment_folder = 'output'


parameters = AnimalParameters(a, b, c, d)
options = GridOptions(
    col_num, row_num, initial_num_predators, initial_num_prey,
    movement_at_edge_choice = 'ne',
    predator_reproduction_choice = 'ipd',
    seed = resolve_seed (),
)
exops = ExperimentOptions(
    data_folder = data_folder,
    experiment_name = experiment_name,
    num_turns = num_turns,
)

if __name__ == '__main__':
    cook = Recipes()
    # DT, ld = cook.run_and_display_multiple(
    #     graph_options = options,
    #     animal_parameters = parameters,
    #     experiment_options = exops,
    #     number_of_experiments = 5,
    #     same_initial_conditions = False,
    # )
    displayer = cook.run_and_display(
        grid_options = options,
        animal_parameters = parameters,
        experiment_options = exops,
    )

    displayer. show_populations_plot ()

    # displayer.save_all_plots()

