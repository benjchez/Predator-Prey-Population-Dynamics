from dataclasses import dataclass

@dataclass
class ExperimentOptions:
    data_folder: str
    experiment_name: str
    num_turns: int