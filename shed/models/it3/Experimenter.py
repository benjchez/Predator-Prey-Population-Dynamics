import copy
from dataclasses import asdict
import io
import pandas as pd

from Grid import Grid
from GraphOptions import GraphOptions
from AnimalParameters import AnimalParameters
from ExperimentOptions import ExperimentOptions
from ExperimentData import ExperimentData

class Experimenter:
    """Different methods to conduct experiments and output results.
    """

    def __init__(self, o: GraphOptions, p: AnimalParameters, e: ExperimentOptions):
        self.o = o
        self.p = p
        self.e = e

    def run_experiment(self) -> ExperimentData:
        grid = Grid(self.o, self.p)
        data = self.run_experiment_from_grid(grid)
        return data
        

    def run_experiment_from_grid(self, g: Grid) -> ExperimentData:

        grid = copy.deepcopy(g)

        paramd = {'Animal options': asdict(self.p),
                  'Graph options': asdict(self.o),
                  'Experiment options': asdict(self.e)}
        
        popd = f"""Time step,Prey number,Predator number\n0,{grid.init_prey},{grid.init_pred}"""

        grid_data = {'timestamp0': copy.deepcopy(grid.grid)}
        
        prey_count = 0
        for i in range(self.e.num_turns):
            # Stop exponential growth
            if prey_count > 100 * grid.init_prey:
                break
            
            turn = i + 1
            grid.turn()
            prey_count, predator_count = grid.an_count()
            popd += f'\n{turn},{prey_count},{predator_count}'
            grid_data['timestamp' + str(turn)] = copy.deepcopy(grid
            .grid)

        popd_csv = io.StringIO(popd)
        popd_df = pd.read_csv(popd_csv, sep = ',')

        graphd_df = pd.DataFrame(grid_data)

        data = ExperimentData(
            popd = popd_df,
            graphd = graphd_df,
            paramd = paramd,
        )

        return data     

    def out_to_files(self):
        """Runs the experiment and outputs to file.\n
        It puts the prey and predator counts per turn into\n
        file with syntax:\n
        turn prey_count predator_count\n
        and puts grid into file_name_grid as json. Puts parameters into json file and\n
          creates empty notes file.
        """
        data = self.run_experiment()
        data.to_files(self.e.experiment_name)
    
    def run_experiments_same_parameters_diff_ic(
            self,
            number_of_experiments: int
    ) -> list[ExperimentData]:
        list_of_ED = [] # List of data from experiments

        experiment_name = self.e.experiment_name

        for i in range(number_of_experiments):
            self.e.experiment_name = experiment_name + "_" + str(i)
            list_of_ED.append(self.run_experiment())
        
        return list_of_ED
    
    def run_experiments_same_parameters_and_ic(
            self,
            number_of_experiments: int
    ) -> list[ExperimentData]:
        list_of_ED = [] # List of data from experiments

        init_grid = Grid(self.o, self.p)

        experiment_name = self.e.experiment_name

        for i in range(number_of_experiments):
            self.e.experiment_name = experiment_name + "_" + str(i)
            list_of_ED.append(self.run_experiment_from_grid(init_grid))
        
        return list_of_ED