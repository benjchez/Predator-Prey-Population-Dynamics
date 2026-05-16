"""Contains classes: AnalysisData and FiledAnalysisData
"""

import json
from pathlib import Path

class AnalysisData:
    """Class containing the data from the analysis of experiment data.
    """

    pmd: list | None
    infod: dict
    notesd: str
    lite: bool

    def __init__(
            self,
            pmd: list | None,
            infod: dict,
            notesd: str,
            lite: bool = False,
        ):

        self. pmd = pmd
        self. infod = infod
        self. notesd = notesd
        self. lite = lite

    @classmethod
    def from_files(
        cls,
        data_folder: str,
        experiment_name: str,
        lite: bool = False
    ):
        
        dir = Path(__file__).parent / 'data' / data_folder / experiment_name / 'analysis'

        infof = dir / 'info.json'
        pmf = dir / 'pointmap.json'
        notesf = dir / 'notes.txt'

        with open(infof, 'r') as file:
            infod = json.load(file)

        if not lite:
            with open(pmf, 'r') as file:
                pmd = json.load(file)

        else:
            pmd = None

        with open(notesf, 'r') as file:
            notesd = file.read()

        return cls(
            pmd = pmd,
            infod = infod,
            notesd = notesd,
            lite = lite,
        )
    
    def to_files(
        self,
        experiment_name: str,
        data_folder: str,
    ) -> 'FiledAnalysisData':
        """Saves analysis data to file."""

        if self. lite:
            raise ValueError ('Cannot save AnalysisData when in lite mode.')
        
        dir = Path(__file__).parent / 'data' / data_folder / experiment_name / 'analysis'

        # Makes directory and fails if it already exists
        dir. mkdir (parents = True)

        pmf = dir / 'pointmap.json'
        infof = dir / 'info.json'
        notesf = dir / 'notes.txt'

        with open(pmf, 'w') as file:
            json.dump(self.pmd, file)

        with open(infof, 'w') as file:
            json.dump(self.infod, file)

        with open(notesf, 'w') as file:
            file.write(self.notesd)

        FAD = FiledAnalysisData(
            d = self,
            data_folder = data_folder,
            experiment_name = experiment_name,
        )

        return FAD

class FiledAnalysisData:
    d: AnalysisData
    dir: Path
    infof: Path
    pmf: Path
    notesf: Path
    lite: bool

    def __init__(
            self,
            d: AnalysisData,
            data_folder: str,
            experiment_name: str,
    ):
        self.d = d
        self.dir = Path(__file__).parent / 'data' / data_folder / experiment_name / 'analysis'

        self.notesf = self.dir / "notes.txt"
        self.infof = self.dir / 'info.json'
        self.pmf = self.dir / 'pointmap.json'

        self. lite = d. lite

    @classmethod
    def from_files(
            cls,
            data_folder: str,
            experiment_name: str,
            lite: bool = False,
    ):
        ad = AnalysisData.from_files(
            data_folder = data_folder,
            experiment_name = experiment_name,
            lite = lite,
        )
        return cls(d = ad,
                   data_folder = data_folder,
                   experiment_name = experiment_name,
                   )

    def write_notes(self, text):
        self.d.notesd = text
        with open(self.notesf, 'w') as file:
            file.write(self.d.notesd)