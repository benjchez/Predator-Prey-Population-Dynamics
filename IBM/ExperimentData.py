"""File containing class ExperimentData and FiledExperimentData
"""

from pathlib import Path
import json

import pandas as pd

class ExperimentData:

    popd: pd.DataFrame
    graphd: pd.DataFrame | None
    paramd: dict
    lite: bool # In lite mode graphd is None


    def __init__(
            self,
            popd: pd.DataFrame,
            graphd: pd.DataFrame | None,
            paramd: dict,
            lite: bool = False,
    ):
        self.popd = popd
        self.graphd = graphd
        self.paramd = paramd
        self. lite = lite
    
    @classmethod
    def from_files(
        cls,
        data_folder: str,
        experiment_name: str,
        lite: bool = False,
    ):

        dir = Path(__file__).parent / 'data' / data_folder / experiment_name / 'raw'

        pop_file = "pop.dat"
        graph_file = "graph.json"
        param_file = "params.json"

        popf = dir / pop_file
        graphf = dir / graph_file
        paramf = dir / param_file

        popd = pd.read_csv(popf)

        if not lite:
            graphd = pd.read_json(graphf)
        else:
            graphd = None
        
        with open(paramf, 'r') as file:
            paramd = json.load(file)

        return cls(popd, graphd, paramd, lite)
    
    def to_files(
            self,
    ) -> 'FiledExperimentData':
        """Writes the experiment data to file.
        
        It saves the data under data / {data_folder} / {experiment_name} / raw.
        
        If there is raw data already stored, it will raise an error.
        
        It will make the parent directories if they don't exist."""

        if self. lite:
            raise ValueError ('Cannot save lite ExperimentData')

        experiment_name: str = self. paramd ['Experiment options'] ['experiment_name']

        data_folder: str = self. paramd ['Experiment options'] ['data_folder']

        dir = Path (__file__). parent / 'data' / data_folder / experiment_name / 'raw'

        # Makes the directory but fails if it already exists
        dir. mkdir (parents = True)

        pop_file = "pop.dat"
        graph_file = "graph.json"
        param_file = "params.json"

        popf = dir / pop_file
        graphf = dir / graph_file
        paramf = dir / param_file

        self.popd.to_csv(popf)

        assert self.graphd is not None
        
        with open(graphf, 'w') as file:
            self.graphd.to_json(file)
            
        with open(paramf, 'w') as file:
            json.dump(self.paramd, file)

        FED = FiledExperimentData(
            d = self,
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
    lite: bool

    def __init__(
            self,
            d: ExperimentData,
        ):
        """Initialise the class by inputting the experiment data and the info about where it is stored.

        Args:
            d (ExperimentData): Data from an experiment.
            data_folder (str): Which folder within the data folder is the experiment stored in.
        """

        experiment_name = d. paramd ['Experiment options'] ['experiment_name']

        data_folder = d. paramd ['Experiment options'] ['data_folder']

        self. dir = Path (__file__). parent / 'data' / data_folder / experiment_name / 'raw'

        pop_file = "pop.dat"
        graph_file = "graph.json"
        param_file = "params.json"

        self.popf = self.dir / pop_file
        self.graphf = self.dir / graph_file
        self.paramf = self.dir / param_file

        self. lite = d. lite

        self.d = d
    

    @classmethod
    def from_files(
        cls,
        data_folder: str,
        experiment_name: str,
        lite: bool = False,
    ):

        data = ExperimentData.from_files(data_folder, experiment_name, lite)

        return cls(data)