"""Contains classes: AnalysisData and FiledAnalysisData
"""

import json
from pathlib import Path
import os

class AnalysisData:
    """Class containing the data from the analysis of experiment data.
    """

    pmd: list
    infod: dict
    notesd: str

    def __init__(
            self,
            pmd: list,
            infod: dict,
            notesd: str,
        ):

        self.pmd = pmd
        self.infod = infod
        self.notesd = notesd

    @classmethod
    def from_files(
        cls,
        data_folder: str,
        experiment_name: str,
    ):
        
        dir = Path(__file__).parent / 'data' / data_folder / experiment_name / 'analysis'

        infof = dir / 'info.json'
        pmf = dir / 'pointmap.json'
        notesf = dir / 'notes.txt'

        with open(infof, 'r') as file:
            infod = json.load(file)

        with open(pmf, 'r') as file:
            pmd = json.load(file)

        with open(notesf, 'r') as file:
            notesd = file.read()

        return cls(
            pmd = pmd,
            infod = infod,
            notesd = notesd,
        )
    
    def to_files(
        self,
        experiment_name: str,
        data_folder: str = 'output',
    ) -> 'FiledAnalysisData':
        dir = Path(__file__).parent / 'data' / data_folder / experiment_name / 'analysis'

        pmf = dir / 'pointmap.json'
        infof = dir / 'info.json'
        notesf = dir / 'notes.txt'

        os.makedirs(dir, exist_ok = True)

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

    @classmethod
    def from_files(
            cls,
            data_folder: str,
            experiment_name: str,
    ):
        ad = AnalysisData.from_files(
            data_folder = data_folder,
            experiment_name = experiment_name,
        )
        return cls(d = ad,
                   data_folder = data_folder,
                   experiment_name = experiment_name,
                   )

    def write_notes(self, text):
        self.d.notesd = text
        with open(self.notesf, 'w') as file:
            file.write(self.d.notesd)