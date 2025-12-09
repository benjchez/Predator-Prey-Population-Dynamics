from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class Analyser:
    def __init__(self, path_to_experiment, name_of_experiment):

        self.dir = Path(__file__).parent / 'data' / path_to_experiment
        dat_file = name_of_experiment + ".dat"
        json_file = name_of_experiment + ".json"
        self.datf = self.dir / dat_file
        self.jsonf = self.dir / json_file

        self.nums = pd.read_csv(self.datf, sep = ' ', header = None)
        column_names = ['Time step', 'Prey number', 'Predator number']
        self.nums.columns = column_names
        self.gd = pd.read_json(self.jsonf)

        # Check if these are the right way round
        self.rn = len(self.gd['timestamp0'])
        self.cn = len(self.gd['timestamp0'][0])

        self.point_map()
    
    def plt_nums(self):
        fig, ax = plt.subplots()
        ax.plot(self.nums['Time step'], self.nums['Prey number'], 'b', label = 'Prey')
        ax.plot(self.nums['Time step'], self.nums['Predator number'], 'r', label = 'Predators')
        ax.set_xlabel('Time step')
        ax.set_ylabel('Population number')
        ax.grid(True)
        ax.legend()
        return fig
    
    def pmft(self, timestamp: int) -> np.ndarray:
        """Returns the point map at a fixed time timestamp as a numpy array.

        Args:
            timestamp (int): fixed time

        Returns:
            np.ndarray: array ready to be used as an image.
        """
        return np.array(self.pm[timestamp])
    
    def point_map(self):
        point_map = []

        num_time_stamps = len(self.gd.columns)

        max_num = 0

        for t in range(num_time_stamps):
            graph = self.gd['timestamp' + str(t)]
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

        self.nts = num_time_stamps
        self.pm = point_map