import json
import copy
import os
from pathlib import Path

from Grid import Grid
from GraphOptions import GraphOptions
from AnimalParameters import AnimalParameters
from ExperimentOptions import ExperimentOptions

class Experimenter:
    """Different methods to conduct experiments and output results.
    """
    def __init__(self, o: GraphOptions, p: AnimalParameters, e: ExperimentOptions):
        self.nt = e.num_turns
        self.g = Grid(o, p) 
        self.dir = Path(__file__).parent / "data" / "output" / e.experiment_name
        dat_file = e.experiment_name + ".dat"
        json_file = e.experiment_name + ".json"
        self.datf = self.dir / dat_file
        self.jsonf = self.dir / json_file
        os.makedirs(self.dir, exist_ok = True)

    # Run experiment with standard out
    def out_to_std(self):
        """Prints the prey count and predator count for the experiment per turn.
        """
        print(f'Initial, Prey count: {self.g.init_prey}, Predator count: {self.g.init_prey}')

        for i in range(self.nt):
            turn = i + 1
            self.g.turn()
            prey_count, predator_count = self.g.an_count()
            print(f'Turn: {turn}, Prey count: {prey_count}, Predator count: {predator_count}')

    def out_to_files(self):
        """Outputs the results from the experiment.\n
        It puts the prey and predator counts per turn into\n
        file with syntax:\n
        turn prey_count predator_count\n
        and puts grid into file_name_grid as json.
        """
        with open(self.datf, 'w') as file:
            file.write(f'0 {self.g.init_prey} {self.g.init_pred}')

            grid_data = {'timestamp1': copy.deepcopy(self.g.grid)}
            
            prey_count = 0
            for i in range(self.nt):

                # Stop exponential growth
                if prey_count > 100 * self.g.init_prey:
                    break
                
                turn = i + 1
                self.g.turn()
                prey_count, predator_count = self.g.an_count()
                file.write(f'\n{turn} {prey_count} {predator_count}')
                grid_data['timestamp' + str(i)] = copy.deepcopy(self.g.grid)

        with open(self.jsonf, 'w') as file_grid:
            json.dump(grid_data, file_grid)
