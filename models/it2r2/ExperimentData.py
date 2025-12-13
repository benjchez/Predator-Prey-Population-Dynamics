from pathlib import Path
import json
import os

import pandas as pd

class ExperimentData:
    graphd: pd.DataFrame

    def __init__(self, popd, graphd, paramd, notesd):
        self.popd = popd
        self.graphd = graphd
        self.paramd = paramd
        self.notesd = notesd
    
    @classmethod
    def from_files(cls, data_folder, experiment_name):
        dir = Path(__file__).parent / 'data' / data_folder

        pop_file = experiment_name + "_pop.dat"
        graph_file = experiment_name + "_graph.json"
        param_file = experiment_name + "_params.json"
        notes_file = experiment_name + "_notes.txt"

        popf = dir / pop_file
        graphf = dir / graph_file
        paramf = dir / param_file
        notesf = dir / notes_file

        popd = pd.read_csv(popf, sep = ' ', header = None)
        column_names = ['Time step', 'Prey number', 'Predator number']
        popd.columns = column_names

        graphd = pd.read_json(graphf)
        
        with open(paramf, 'r') as file:
            paramd = json.load(file)
        
        with open(notesf, 'r') as file:
            notesd = file.read()

        return cls(popd, graphd, paramd, notesd)
    
    def to_files(self, experiment_name, data_folder = 'output'):
        dir = Path(__file__).parent / 'data' / data_folder / experiment_name
        os.makedirs(dir, exist_ok = True)

        pop_file = experiment_name + "_pop.dat"
        graph_file = experiment_name + "_graph.json"
        param_file = experiment_name + "_params.json"
        notes_file = experiment_name + "_notes.txt"

        popf = dir / pop_file
        graphf = dir / graph_file
        paramf = dir / param_file
        notesf = dir / notes_file

        with open(popf, 'w') as file:
            file.write(self.popd)
        
        with open(graphf, 'w') as file:
            json.dump(self.graphd, file)

        with open(paramf, 'w') as file:
            json.dump(self.paramd, file)
        
        with open(notesf, 'w') as file:
            file.write(self.notesd)