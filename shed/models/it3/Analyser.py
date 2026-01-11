from ExperimentData import ExperimentData, FiledExperimentData
from AnalysisData import AnalysisData

class Analyser:
    """A class for analysing data from an experiment.

    On initialisation it will get the experiment data from file and create a point map.

    Attributes:
        fd (FiledExperimentData): the experiment data connected to the files it is saved in.
        d (ExperimentData): the experiment data
    """

    ed: ExperimentData
    rn: int
    cn: int
    
    def __init__(self, ed: ExperimentData):
        """Initialise the analyser with data from a previous experiment.

        Args:
            rel_path_to_experiment (str): the path to the experiment (and including) the experiment folder from (and not including) the data folder for the model
            name_of_experiment (str): the name of the experiment (ie the name of the folder that the experiment is saved in)
        """

        self.ed = ed

        self.cn = self.ed.paramd['Graph options']['col_num']
        self.rn = self.ed.paramd['Graph options']['row_num']

    @classmethod
    def from_files(
        cls,
        rel_path_to_experiment: str,
        name_of_experiment: str
    ):
        
        FED = FiledExperimentData.from_files(
            data_folder = rel_path_to_experiment,
            experiment_name = name_of_experiment,
        )
        
        return(cls(ed = FED.d))
    
    def analyse(self) -> AnalysisData:
        pm, info = self.point_map()
        ad = AnalysisData(
            pmd = pm,
            infod = info,
            notesd = '',
        )

        return ad      
    
    def point_map(self) -> tuple[list, dict]:
        point_map = []
        info = {}

        num_time_stamps = len(self.ed.graphd.columns)

        max_num = 0

        for t in range(num_time_stamps):
            graph = self.ed.graphd['timestamp' + str(t)]
            point_map.append([[[0, 0, 0] for _ in range(self.rn)] for _ in range(self.cn)])
            for row in range(self.rn):
                for column in range(self.cn):
                    point = graph[row][column]
                    for animal in point:
                        if animal == 'prey':
                            point_map[t][row][column][2] += 1
                        else:
                            point_map[t][row][column][0] += 1

                    pred_num = point_map[t][row][column][0]
                    prey_num = point_map[t][row][column][2]      


                    total_num = pred_num + prey_num

                    if total_num > max_num:
                        max_num = total_num
        
        scale = 1 / max_num * 10

        for t in range(num_time_stamps):
            for row in range(self.rn):
                for column in range(self.cn):
                    point_map[t][row][column][0] *= scale
                    point_map[t][row][column][2] *= scale

        info['number of time stamps'] = num_time_stamps

        return point_map, info