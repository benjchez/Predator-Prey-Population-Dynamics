"""File containing class ExperimentData and FiledExperimentData
"""

from pathlib import Path
import json
import os

import pandas as pd

class ExperimentData:

    popd: pd.DataFrame
    graphd: pd.DataFrame
    paramd: dict


    def __init__(
            self,
            popd: pd.DataFrame,
            graphd: pd.DataFrame,
            paramd: dict,
        ):
        self.popd = popd
        self.graphd = graphd
        self.paramd = paramd
    
    @classmethod
    def from_files(cls, data_folder, experiment_name):
        dir = Path(__file__).parent / 'data' / data_folder / experiment_name / 'experiment'

        pop_file = experiment_name + "_pop.dat"
        graph_file = experiment_name + "_graph.json"
        param_file = experiment_name + "_params.json"

        popf = dir / pop_file
        graphf = dir / graph_file
        paramf = dir / param_file

        popd = pd.read_csv(popf)

        graphd = pd.read_json(graphf)
        
        with open(paramf, 'r') as file:
            paramd = json.load(file)

        return cls(popd, graphd, paramd)
    
    def to_files(
            self,
            experiment_name: str,
            data_folder: str = 'output'
        ) -> 'FiledExperimentData':

        dir = Path(__file__).parent / 'data' / data_folder / experiment_name / 'experiment'
        os.makedirs(dir, exist_ok = True)

        pop_file = experiment_name + "_pop.dat"
        graph_file = experiment_name + "_graph.json"
        param_file = experiment_name + "_params.json"

        popf = dir / pop_file
        graphf = dir / graph_file
        paramf = dir / param_file

        self.popd.to_csv(popf)
        
        with open(graphf, 'w') as file:
            self.graphd.to_json(file)

        with open(paramf, 'w') as file:
            json.dump(self.paramd, file)

        FED = FiledExperimentData(
            d = self,
            data_folder = data_folder,
            experiment_name = experiment_name,
        )

        return FED
    
class FiledExperimentData:
    """Class containing (already) filed experiment data and info about its storage.
    """
    
    dir: Path
    popf: Path
    graphf: Path
    paramf: Path
    notesf: Path
    d: ExperimentData

    def __init__(
            self,
            d: ExperimentData,
            data_folder: str,
            experiment_name:str,
        ):
        """Initialise the class by inputting the experiment data and the info about where it is stored.

        Args:
            d (ExperimentData): Data from an experiment.
            data_folder (str): Which folder within the data folder is the experiment stored in.
            experiment_name (str): What name is the experiment stored under (ie what is the name of the folder that the experiment is contained within).
        """
        self.dir = Path(__file__).parent / 'data' / data_folder / experiment_name / 'experiment'

        pop_file = experiment_name + "_pop.dat"
        graph_file = experiment_name + "_graph.json"
        param_file = experiment_name + "_params.json"

        self.popf = self.dir / pop_file
        self.graphf = self.dir / graph_file
        self.paramf = self.dir / param_file

        self.d = d

    @classmethod
    def from_files(cls, data_folder, experiment_name):
        data = ExperimentData.from_files(data_folder, experiment_name)
        return cls(data, data_folder, experiment_name)