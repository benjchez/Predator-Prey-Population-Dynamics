from Analyser import Analyser
from AnimalParameters import AnimalParameters
from DisplayAnalysis import DisplayAnalysis
from DisplayTogether import DisplayTogether
from EnAData import EnAData, FiledEnAData
from ExperimentData import ExperimentData
from Experimenter import Experimenter
from ExperimentOptions import ExperimentOptions
from Grid import Grid
from GridOptions import GridOptions

class Recipes:
    """This class provides useful functions to complete and retrieve experiments.
    """

    def display_from_files(
            self,
            data_folder: str,
            experiment_name: str,
        ) -> DisplayAnalysis:

        """Finds an experiment from file and returns a displayer object that can be used to display and analyse the results.

        Args:
            data_folder (str): folder in which the experiment is stored in
            experiment_name (str): name of the experiment

        Returns:
            DisplayAnalysis: a displayer object to display the results of the experiment
        """

        FEnAD = FiledEnAData.from_files(
            data_folder = data_folder,
            experiment_name = experiment_name,
        )

        displayer = DisplayAnalysis(
            FEnAD = FEnAD,
        )

        return displayer

    def run_and_display(
            self,
            grid_options: GridOptions,
            animal_parameters: AnimalParameters,
            experiment_options: ExperimentOptions,
    ) -> DisplayAnalysis:
        
        """Function that runs an experiment and returns a display object to display the results.

        Args:
            grid_options (GridOptions): graph-related experiment parameters
            animal_parameters (AnimalParameters): animal-related experiment parameters
            experiment_options (ExperimentOptions): experiment options

        Returns:
            DisplayAnalysis: a display object to be used to display the results of the experiment
        """

        experiment = Experimenter(
            o = grid_options,
            p = animal_parameters,
            e = experiment_options,
        )
        ed = experiment.run_experiment()

        analyse = Analyser(
            ed = ed
        )
        ad = analyse.analyse()

        EnAD = EnAData(
            ed = ed,
            ad = ad,
        )

        FEnAD = EnAD.to_files()

        displayer = DisplayAnalysis(
            FEnAD = FEnAD
        )

        return displayer
    

    def run_and_display_multiple(
            self,
            grid_options: GridOptions,
            animal_parameters: AnimalParameters,
            experiment_options: ExperimentOptions,
            number_of_experiments: int,
            same_initial_conditions: bool = True,
    ) -> DisplayTogether:
        
        """Runs multiple experiments and returns objects that allow you to display the results together or individually.

        Each experiment is saved under <experiment>_i where i is the ith experiment with index starting at one.

        Args:
            grid_options (GridOptions): grid options
            animal_parameters (AnimalParameters): animal parameters
            experiment_options (ExperimentOptions): experiment options
            number_of_experiments (int): number of experiments to conduct
            same_initial_conditions (bool, optional): Do you want the experiments to start with the same grid initially? Defaults to True.

        Returns:
            DisplayTogether: A DisplayTogether object
        """

        list_of_displayers: list[DisplayAnalysis] = []

        experiment = Experimenter(
            o = grid_options,
            p = animal_parameters,
            e = experiment_options,
        )

        name = experiment_options. experiment_name

        if same_initial_conditions:
            list_of_ed = experiment.run_experiments_same_parameters_and_ic(
                number_of_experiments = number_of_experiments,
            )

        else:
            list_of_ed = experiment.run_experiments_same_parameters_diff_ic(
                number_of_experiments = number_of_experiments,
            )

        for ed in list_of_ed:
            analyse = Analyser(
                ed = ed,
            )
            ad = analyse.analyse()

            EnAD = EnAData(
                ed = ed,
                ad = ad,
            )

            FEnAD = EnAD.to_files()

            displayer = DisplayAnalysis(
                FEnAD = FEnAD
            )

            list_of_displayers.append(displayer)

        

        DT = DisplayTogether (
            list_of_displayers = list_of_displayers,
            name = name,
        )

        return DT
        

def analyse_and_save_EnAD (
        ed: ExperimentData,
):
    analyse = Analyser(
        ed = ed,
    )
    
    ad = analyse.analyse()

    EnAD = EnAData(
        ed = ed,
        ad = ad,
    )
    
    EnAD.to_files()

def run_and_save (
        grid_options: GridOptions,
        animal_parameters: AnimalParameters,
        experiment_options: ExperimentOptions,            
):
    e = Experimenter (o = grid_options, p = animal_parameters, e = experiment_options)

    exp_data = e. run_experiment ()

    analyse_and_save_EnAD (ed = exp_data)

def run_and_save_multiple (
        grid_options: GridOptions,
        animal_parameters: AnimalParameters,
        experiment_options: ExperimentOptions,
        number_of_experiments: int,
        same_initial_conditions: bool = True,
):
    experiment = Experimenter(
        o = grid_options,
        p = animal_parameters,
        e = experiment_options,
    )

    if same_initial_conditions:
        list_of_ed = experiment.run_experiments_same_parameters_and_ic(
            number_of_experiments = number_of_experiments,
        )

    else:
        list_of_ed = experiment.run_experiments_same_parameters_diff_ic(
            number_of_experiments = number_of_experiments,
        )

    for ed in list_of_ed:
        analyse_and_save_EnAD (ed = ed)

def run_and_save_multiple_one_at_a_time (
        grid_options: GridOptions,
        animal_parameters: AnimalParameters,
        experiment_options: ExperimentOptions,
        number_of_experiments: int,
        same_initial_conditions: bool = True,
):
    experiment = Experimenter(
        o = grid_options,
        p = animal_parameters,
        e = experiment_options,
    )

    experiment_name = experiment.e.experiment_name

    if same_initial_conditions:

        grid = Grid(experiment.o, experiment.p)

        for i in range(1, number_of_experiments + 1):

            experiment.e.experiment_name = experiment_name + "_" + str(i)
            
            if i == 1:
                ed = experiment. run_experiment_from_grid (
                    g = grid
                )
            else:
                ed = experiment. run_experiment_from_grid (
                    g = grid,
                    use_random_seed = True,
                    seed_starts_after_turn = 0,
                )

            analyse_and_save_EnAD (ed = ed)

            print (experiment. e. experiment_name, 'done')


    else:

        for i in range(1, number_of_experiments + 1):
            
            experiment.e.experiment_name = experiment_name + "_" + str(i)            

            if i == 1:
                ed = experiment. run_experiment ()
            
            else:
                ed = experiment. run_experiment (
                    use_random_seed = True,
                )

            analyse_and_save_EnAD (ed = ed)

            print (experiment. e. experiment_name, 'done')

    experiment.e.experiment_name = experiment_name