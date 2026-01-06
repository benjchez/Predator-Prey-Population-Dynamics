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
        self.nt = e.num_turns
        self.g = Grid(o, p)

    def run_experiment(self) -> ExperimentData:
        paramd = {'Animal options': asdict(self.p),
                  'Graph options': asdict(self.o),
                  'Experiment options': asdict(self.e)}

        popd = f"""Time step,Prey number,Predator number\n0,{self.g.init_prey},{self.g.init_pred}"""

        grid_data = {'timestamp0': copy.deepcopy(self.g.grid)}
        
        prey_count = 0
        for i in range(self.nt):
            # Stop exponential growth
            if prey_count > 100 * self.g.init_prey:
                break
            
            turn = i + 1
            self.g.turn()
            prey_count, predator_count = self.g.an_count()
            popd += f'\n{turn},{prey_count},{predator_count}'
            grid_data['timestamp' + str(turn)] = copy.deepcopy(self.g.grid)

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
        """Outputs the results from the experiment.\n
        It puts the prey and predator counts per turn into\n
        file with syntax:\n
        turn prey_count predator_count\n
        and puts grid into file_name_grid as json. Puts parameters into json file and\n
          creates empty notes file.
        """
        paramd = {'Animal options': asdict(self.p),
                  'Graph options': asdict(self.o),
                  'Experiment options': asdict(self.e)}

        popd = f'0 {self.g.init_prey} {self.g.init_pred}'

        grid_data = {'timestamp0': copy.deepcopy(self.g.grid)}
        
        prey_count = 0
        for i in range(self.nt):
            # Stop exponential growth
            if prey_count > 100 * self.g.init_prey:
                break
            
            turn = i + 1
            self.g.turn()
            prey_count, predator_count = self.g.an_count()
            popd += f'\n{turn} {prey_count} {predator_count}'
            grid_data['timestamp' + str(i)] = copy.deepcopy(self.g.grid)

        popd_csv = io.StringIO(popd)
        popd_df = pd.read_csv(popd_csv)

        graphd_df = pd.DataFrame(grid_data)

        data = ExperimentData(
            popd = popd_df,
            graphd = graphd_df,
            paramd = paramd,
        )

        data.to_files(self.e.experiment_name)