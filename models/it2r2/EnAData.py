"""File containing the classes EnAdata and FiledEnAdata
"""

from pathlib import Path

from ExperimentData import ExperimentData, FiledExperimentData
from AnalysisData import AnalysisData, FiledAnalysisData

class EnAData:
    ed: ExperimentData
    ad: AnalysisData

    def __init__(
            self,
            ed: ExperimentData,
            ad: AnalysisData,
    ):
        self.ed = ed
        self.ad = ad

    @classmethod
    def from_files(
        cls,
        data_folder: str,
        experiment_name: str,
    ):
        
        ED = ExperimentData.from_files(
            data_folder = data_folder,
            experiment_name = experiment_name,
        )
        AD = AnalysisData.from_files(
            data_folder = data_folder,
            experiment_name = experiment_name,
        )

        return cls(ed = ED, ad = AD)
    
    def to_files(
            self,
            experiment_name: str,
            data_folder: str = 'output',
    ) -> 'FiledEnAData':
        
        self.ed.to_files(
            experiment_name = experiment_name,
            data_folder = data_folder,
        )

        self.ad.to_files(
            experiment_name = experiment_name,
            data_folder = data_folder,
        )
        
        FEnAD = FiledEnAData(
            ed = self.ed,
            ad = self.ad,
            data_folder = data_folder,
            experiment_name = experiment_name,
        )

        return FEnAD

class FiledEnAData:
    """Class containing filed experiment and analysis data and the info about its storage.
    """
    
    FED: FiledExperimentData
    FAD: FiledAnalysisData
    dir: Path

    def __init__(
            self,
            ed: ExperimentData,
            ad: AnalysisData,
            data_folder: str,
            experiment_name: str,
    ):
        FED = FiledExperimentData(
            d = ed,
            data_folder = data_folder,
            experiment_name = experiment_name,
        )
        FAD = FiledAnalysisData(
            d = ad,
            data_folder = data_folder,
            experiment_name = experiment_name,
        )
        
        self.dir = FED.dir.parent

        self.FED = FED
        self.FAD = FAD

    @classmethod
    def from_files(
            cls,
            data_folder: str,
            experiment_name: str,
    ):
        EnAD = EnAData.from_files(
            data_folder = data_folder,
            experiment_name = experiment_name,
        )
        return cls(ed = EnAD.ed,
                   ad = EnAD.ad,
                   data_folder = data_folder,
                   experiment_name = experiment_name,
                   )
