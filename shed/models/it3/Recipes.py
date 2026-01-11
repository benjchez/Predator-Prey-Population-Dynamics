from pathlib import Path

from Analyser import Analyser
from AnimalParameters import AnimalParameters
from DisplayAnalysis import DisplayAnalysis
from DisplayTogether import DisplayTogether
from EnAData import EnAData, FiledEnAData
from Experimenter import Experimenter
from ExperimentOptions import ExperimentOptions
from GraphOptions import GraphOptions

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
            graph_options: GraphOptions,
            animal_parameters: AnimalParameters,
            experiment_options: ExperimentOptions,
    ) -> DisplayAnalysis:
        
        """Function that runs an experiment and returns a display object to display the results.

        Args:
            graph_options (GraphOptions): graph-related experiment parameters
            animal_parameters (AnimalParameters): animal-related experiment parameters
            experiment_options (ExperimentOptions): experiment options

        Returns:
            DisplayAnalysis: a display object to be used to display the results of the experiment
        """

        experiment = Experimenter(
            o = graph_options,
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
            graph_options: GraphOptions,
            animal_parameters: AnimalParameters,
            experiment_options: ExperimentOptions,
            number_of_experiments: int,
            same_initial_conditions: bool = True,
    ) -> tuple[DisplayTogether, list[DisplayAnalysis]]:
        
        """Runs multiple experiments and returns objects that allow you to display the results together or individually.

        Each experiment is saved under <experiment>_i where i is the ith experiment with index starting at zero.

        Args:
            graph_options (GraphOptions): grid options
            animal_parameters (AnimalParameters): animal parameters
            experiment_options (ExperimentOptions): experiment options
            number_of_experiments (int): number of experiments to conduct
            same_initial_conditions (bool, optional): Do you want the experiments to start with the same grid initially? Defaults to True.

        Returns:
            tuple[DisplayTogether, list[DisplayAnalysis]]: A DisplayTogether object and a list of Displayers so that you can either display the results together or individually
        """

        list_of_displayers: list[DisplayAnalysis] = []

        experiment = Experimenter(
            o = graph_options,
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

        DT = DisplayTogether.from_displayers(
            list_of_displayers = list_of_displayers,
        )

        return DT, list_of_displayers
    
    def display_consecutives_from_files(
            self,
            data_folder: str,
            root_name: str,
    ) -> tuple[DisplayTogether, list[DisplayAnalysis]]:
        list_of_displayers: list[DisplayAnalysis] = []
        
        i = 0
        while True:
            experiment_name = root_name + "_" + str(i)
            experiment_path = Path(__file__).parent / 'data' / data_folder / experiment_name
            if not(experiment_path.is_dir()):
                break

            displayer = self.display_from_files(
                data_folder = data_folder,
                experiment_name = experiment_name,
            )
            list_of_displayers.append(displayer)
            i += 1
        
        DT = DisplayTogether.from_displayers(
            list_of_displayers = list_of_displayers
        )

        return DT, list_of_displayers
        

