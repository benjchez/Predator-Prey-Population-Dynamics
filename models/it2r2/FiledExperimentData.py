from pathlib import Path

from ExperimentData import ExperimentData

class FiledExperimentData:
    def __init__(self, d: ExperimentData, data_folder, experiment_name):
        self.dir = Path(__file__).parent / 'data' / data_folder

        pop_file = experiment_name + "_pop.dat"
        graph_file = experiment_name + "_graph.json"
        param_file = experiment_name + "_params.json"
        notes_file = experiment_name + "_notes.txt"

        self.popf = self.dir / pop_file
        self.graphf = self.dir / graph_file
        self.paramf = self.dir / param_file
        self.notesf = self.dir / notes_file

        self.d = d

    @classmethod
    def from_files(cls, data_folder, experiment_name):
        data = ExperimentData.from_files(data_folder, experiment_name)
        return cls(data, data_folder, experiment_name)
    
    def write_notes(self, text):
        self.d.notesd = text
        with open(self.notesf, 'w') as file:
            file.write(self.d.notesd)