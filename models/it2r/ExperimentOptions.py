from dataclasses import dataclass

@dataclass
class ExperimentOptions:
    experiment_name: str
    num_turns: int