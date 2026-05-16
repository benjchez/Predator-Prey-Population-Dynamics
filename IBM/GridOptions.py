from dataclasses import dataclass
from typing import Literal

@dataclass
class GridOptions:
    col_num: int # Number of columns
    row_num: int # Number of rows
    init_num_pred: int
    init_num_prey: int
    seed: int
    seed_starts_after_turn: int = -1
    movement_at_edge_choice: Literal ['ne', 'rep'] = 'ne'
    predator_reproduction_choice: Literal ['ipd', 'dpd'] = 'dpd'
    turn_choice: Literal ['d', 'r'] = 'd'