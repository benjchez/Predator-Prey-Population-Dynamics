from pathlib import Path

class DataHandler:
    def __init__(self, pathcurfile = __file__):
        self.par = Path(pathcurfile).parent / 'data'
        self.dfs()

    def dfs(self):
        """Outputs the folders holding data relating to the model.
        """
        folder_list = []
        ab_data_paths = self.par.iterdir()

        for ab_data_path in ab_data_paths:
            # Difference between absolute path and path relative to the parent directory which is the data folder.
            rel_dp = ab_data_path.relative_to(self.par)
            folder_list.append(str(rel_dp))

        self.dfos = folder_list

    def expl(self, dfo: str) -> list[str]:
        """Returns the list of experiments in data folder.

        Args:
            dfo (str): Data folder

        Returns:
            list[str]: List of experiments
        """
        experiment_list = []
        path = self.par / dfo
        ab_experiment_paths = path.iterdir()
        for ab_experiment_path in ab_experiment_paths:
            rel_ep = ab_experiment_path.relative_to(path)
            experiment_list.append(str(rel_ep))
        
        return experiment_list