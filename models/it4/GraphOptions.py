from dataclasses import dataclass

@dataclass
class GraphOptions:
    col_num: int # Number of columns
    row_num: int # Number of rows
    init_num_pred: int
    init_num_prey: int