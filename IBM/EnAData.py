"""File containing the classes EnAdata and FiledEnAdata
"""

from pathlib import Path
import shutil

from ExperimentData import ExperimentData, FiledExperimentData
from AnalysisData import AnalysisData, FiledAnalysisData

class EnAData:
    ed: ExperimentData
    ad: AnalysisData
    lite: bool

    def __init__(
            self,
            ed: ExperimentData,
            ad: AnalysisData,
    ):
        self.ed = ed
        self.ad = ad

        if self. ed. lite or self. ad. lite:
            self. lite = True

        else:
            self. lite = False

    @classmethod
    def from_files(
        cls,
        data_folder: str,
        experiment_name: str,
        lite: bool = False,
    ):
        
        ED = ExperimentData.from_files(
            data_folder = data_folder,
            experiment_name = experiment_name,
            lite = lite,
        )
        AD = AnalysisData.from_files(
            data_folder = data_folder,
            experiment_name = experiment_name,
            lite = lite,
        )

        return cls(ed = ED, ad = AD)
    
    def to_files(
            self,
    ) -> 'FiledEnAData':
        
        if self. lite:
            raise ValueError ('Cannot save EnAData in lite mode')
        
        experiment_name = self.ed.paramd['Experiment options']['experiment_name']

        data_folder = self. ed. paramd ['Experiment options'] ['data_folder']
        
        self. ed. to_files ()

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
    _alive: bool
    lite: bool

    def __init__(
            self,
            ed: ExperimentData,
            ad: AnalysisData,
            data_folder: str,
            experiment_name: str,
    ):
        FED = FiledExperimentData(
            d = ed,
        )
        
        FAD = FiledAnalysisData(
            d = ad,
            data_folder = data_folder,
            experiment_name = experiment_name,
        )
        
        self.dir = FED.dir.parent

        self.FED = FED
        self.FAD = FAD

        self._alive = True

        if ed. lite or ad. lite:
            self. lite = True

        else:
            self. lite = False

    def _check_alive(self):
        if not self._alive:
            raise RuntimeError("experiment has been deleted")

    def delete(self) -> None:
        """Delete this experiment's folder from disk and mark the object as no longer usable."""

        self. _check_alive ()

        if self. lite:
            raise ValueError ('Cannot delete FiledEnAData in lite mode')
     

        target = self. dir

        if not target. exists ():
            raise FileNotFoundError(target)
        
        shutil.rmtree(target)

        self._alive = False

    def move(
            self,
            new_name: str | None = None,
            move_to_folder: str | None = None,
    ) -> None:
        """Move an experiment to another data folder and/or rename it.
        
        move_to_folder must be a single-level folder."""

        self. _check_alive ()

        if self. lite:
            raise ValueError ('Cannot move FiledEnAData in lite mode')

        # Case of nothing changes
        if not new_name and not move_to_folder:
            return

        old_directory = self. dir

        # Extract data
        ED = self. FED. d
        AD = self. FAD. d

        # Change the experiment name
        if new_name:
            ED. paramd ['Experiment options'] ['experiment_name'] = new_name

        else:
            new_name = self. dir. name
        
        if move_to_folder:

            # Check move_to_folder is only one folder
            if len (Path (move_to_folder). parts) != 1:
                raise ValueError ("move_to_folder must be a single-level folder")
            
            ED. paramd ['Experiment options'] ['data_folder'] = move_to_folder
        
        else:
            move_to_folder = self. dir. parent. name
        
        # Check move_to_folder is only one folder
        if len (Path (move_to_folder). parts) != 1:
            raise ValueError ("move_to_folder must be a single-level folder")

        new_directory = Path (__file__). parent / 'data' / move_to_folder / new_name

        # Nothing changes case
        if new_directory. resolve () == old_directory. resolve ():
            return
        
        if new_directory. exists ():
            raise FileExistsError (new_directory)

        EnAD = EnAData (
            ed = ED,
            ad = AD,
        )

        # Save as new FiledEnAData
        new_FEnAD = EnAD. to_files ()

        # Set self to this new instance
        self. FED = new_FEnAD. FED
        self. FAD = new_FEnAD. FAD
        self. dir = new_FEnAD. dir

        # Remove old directory
        shutil. rmtree (old_directory)


    @classmethod
    def from_files(
            cls,
            data_folder: str,
            experiment_name: str,
            lite: bool = False,
    ):
        path_to_experiment = Path (__file__). parent / 'data' / data_folder / experiment_name

        if not path_to_experiment. exists ():
            raise ValueError (f'Experiment with data folder: {data_folder} and experiment name {experiment_name} does not exist.')

        EnAD = EnAData.from_files(
            data_folder = data_folder,
            experiment_name = experiment_name,
            lite = lite,
        )

        return cls(ed = EnAD.ed,
                   ad = EnAD.ad,
                   data_folder = data_folder,
                   experiment_name = experiment_name,
                   )
