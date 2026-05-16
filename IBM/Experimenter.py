import copy
from dataclasses import asdict
import io
import pandas as pd

from Grid import Grid
from GridOptions import GridOptions
from AnimalParameters import AnimalParameters
from ExperimentOptions import ExperimentOptions
from ExperimentData import ExperimentData
from utils import resolve_seed

class Experimenter:
    """Different methods to conduct experiments and output results.
    """

    def __init__(
            self, o: GridOptions,
            p: AnimalParameters,
            e: ExperimentOptions,
    ):
        self.o = o
        self.p = p
        self.e = e

    def run_experiment(
            self,
            use_random_seed: bool = False,
            custom_experiment_options: ExperimentOptions | None = None,
    ) -> ExperimentData:
        
        o = copy. deepcopy (self. o)

        if use_random_seed:
            seed = resolve_seed ()
            o. seed = seed

        grid = Grid (o, self.p)

        data = self. run_experiment_from_grid (
            g = grid,
            custom_grid_options = o,
            custom_experiment_options = custom_experiment_options,
        )

        return data
        

    def run_experiment_from_grid(
            self, g: Grid,
            use_random_seed: bool = False,
            seed_starts_after_turn: int = -1,
            custom_grid_options: GridOptions | None = None,
            custom_experiment_options: ExperimentOptions | None = None,
    ) -> ExperimentData:
        """Use_random_seed will overwite the seed for custom grid options passed."""

        grid = copy.deepcopy(g)


        # Experiment options are only read so don't need to be copied whereas grid options may be altered so are deep copied
      
        if custom_grid_options is not None:
            o = copy. deepcopy (custom_grid_options)
        
        else:
            o = copy. deepcopy (self. o)

        e = self. e if custom_experiment_options is None else custom_experiment_options

        if use_random_seed:

            seed = resolve_seed ()

            grid. rng = grid. get_random_number_generator (seed)

            o. seed = seed
            o. seed_starts_after_turn = seed_starts_after_turn


        

        paramd = {'Animal options': asdict (self.p),
                  'Graph options': asdict (o),
                  'Experiment options': asdict (e)}
        
        initial_pairs = grid. count_pairs ()
        
        popd = f"""Time step,Prey number,Predator number,Predator-prey pairs\n0,{grid.init_prey},{grid.init_pred},{initial_pairs}"""

        grid_data = {'timestamp0': copy.deepcopy(grid.grid)}
        
        prey_count = 0

        for turn in range(1, e. num_turns + 1):
            # Stop exponential growth
            if prey_count > 100 * grid.init_prey:
                break
            
            grid. do_turn ()

            # Count the population numbers
            prey_count, predator_count, pairs_count = grid. stats_count ()
            
            popd += f'\n{turn},{prey_count},{predator_count},{pairs_count}'

            # Take snapshot of grid
            grid_data['timestamp' + str(turn)] = copy.deepcopy (grid.grid)

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
        data. to_files ()
    
    def run_experiments_same_parameters_diff_ic(
            self,
            number_of_experiments: int,
            first_run_uses_experiment_seed: bool = True,
    ) -> list[ExperimentData]:
        list_of_ED = [] # List of data from experiments

        experiment_name = self.e.experiment_name

        for i in range(1, number_of_experiments + 1):

            e = copy. deepcopy (self. e)
            
            e. experiment_name = experiment_name + "_" + str(i)

            if i == 1 and first_run_uses_experiment_seed:
                list_of_ED. append (self. run_experiment (
                    use_random_seed = False,
                    custom_experiment_options = e,
                    ) )

            else:
                list_of_ED. append (self. run_experiment (
                    use_random_seed = True,
                    custom_experiment_options = e,
                    ) )
        
        return list_of_ED
    
    def run_experiments_same_parameters_and_ic(
            self,
            number_of_experiments: int
    ) -> list[ExperimentData]:
        list_of_ED = [] # List of data from experiments

        init_grid = Grid(self.o, self.p)

        experiment_name = self.e.experiment_name

        for i in range(1, number_of_experiments + 1):

            e = copy. deepcopy (self. e)

            e.experiment_name = experiment_name + "_" + str(i)

            list_of_ED. append (
                self. run_experiment_from_grid (
                    g = init_grid,
                    use_random_seed = True,
                    seed_starts_after_turn = 0,
                    custom_experiment_options = e,
                )
            )
        
        return list_of_ED