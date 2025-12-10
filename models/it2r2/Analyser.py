import matplotlib.pyplot as plt
from matplotlib.image import AxesImage
import numpy as np

from FiledExperimentData import FiledExperimentData

class Analyser:
    def __init__(self, rel_path_to_experiment, name_of_experiment):

        self.fd = FiledExperimentData.from_files(data_folder = rel_path_to_experiment, experiment_name = name_of_experiment)

        self.d = self.fd.d

        # TODO: Check if these are the right way round
        self.rn = len(self.d.graphd['timestamp0'])
        self.cn = len(self.d.graphd['timestamp0'][0])

        self.point_map()

    
    def plt_nums(self):
        fig, ax = plt.subplots()
        ax.plot(self.d.popd['Time step'], self.d.popd['Prey number'], 'b', label = 'Prey')
        ax.plot(self.d.popd['Time step'], self.d.popd['Predator number'], 'r', label = 'Predators')
        ax.set_xlabel('Time step')
        ax.set_ylabel('Population number')
        ax.grid(True)
        ax.legend()
        return fig
    
    def show_pmft(self, timestamp: int):
        """Calculate and shows point map at fixed time point.

        Args:
            timestamp (int): Time point
        """
        self.pmft(timestamp)
        plt.show()
    
    def pmft(self, timestamp: int) -> AxesImage:
        """Returns the point map at a fixed time timestamp as an \n
        image.

        Args:
            timestamp (int): fixed time

        Returns:
            AxesImage: pmft image
        """
        pm_ft = self.pm[timestamp]
        arr = np.array(pm_ft)
        image = plt.imshow(arr)
        return image 
    
    
    def point_map(self):
        point_map = []

        num_time_stamps = len(self.d.graphd.columns)

        max_num = 0

        for t in range(num_time_stamps):
            graph = self.d.graphd['timestamp' + str(t)]
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