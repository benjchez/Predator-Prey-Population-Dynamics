from typing import Callable

import numpy as np
from numpy.random import Generator

from AnimalParameters import AnimalParameters
from GridOptions import GridOptions

class Grid:

    edge_function: Callable
    pred_reproduction_function: Callable
    turn_function: Callable
    rng: Generator

    def __init__(self, o: GridOptions, p: AnimalParameters):

        self.init_prey = o.init_num_prey
        self.init_pred = o.init_num_pred
        self.col_num = o.col_num
        self.row_num = o.row_num
        
        self.a = p.a
        self.b = p.b
        self.c = p.c
        self.d = p.d

        self. rng = self. get_random_number_generator (o. seed)

        self. edge_function = self. get_edge_movement_function (o. movement_at_edge_choice)
        self. pred_reproduction_function = self. get_predator_reproduction_function (o. predator_reproduction_choice)

        self. turn_function = self. get_turn_function (o. turn_choice)

        self. grid = self. create_grid ()

    def get_random_number_generator (self, seed: int):

        return np.random. default_rng (seed)

    def get_edge_movement_function (self, movement_at_edge_choice):
        """Get function for how movement at edges will be handled."""

        if movement_at_edge_choice == 'ne': # no escape
            edge_function = self. move_no_escape

        elif movement_at_edge_choice == 'rep': # Random Edge Point
            edge_function = self. move_im_em

        else:
            raise ValueError (f"You gave {movement_at_edge_choice} as your grid movement choice. This isn't a valid choice.")
        
        return edge_function

    def get_predator_reproduction_function (self, pred_reproduction_choice):
        """Get function for how predator spawn and prey death will be handled."""

        # prf - predator reproduction (and prey death) function

        if pred_reproduction_choice == 'ipd': # Independent of Prey Death
            prf = self. predator_spawns_whether_or_not_prey_die
        
        elif pred_reproduction_choice == 'dpd': # dpd - Dependent on Prey Death
            prf = self. predator_spawns_only_if_prey_dies

        else:
            raise ValueError (f"You gave {pred_reproduction_choice} as your predator reproduction choice. This isn't a valid choice.")
        
        return prf

    def get_turn_function (self, turn_choice):

        if turn_choice == 'd':
            turn_function = self. default_turn

        elif turn_choice == 'r':
            turn_function = self. turn_no_movement_and_randomise_placement

        else:
            raise ValueError (f'Your turn choice: {turn_choice} is invalid.')
        
        return turn_function

    def do_turn (self):
        """Run the turn function."""

        self. turn_function ()

    def default_turn (self):

        self. move ()
        self. eating ()
        self. prey_spawn ()
        self. predator_death ()

    def turn_no_movement (self):
        """Runs a turn without any movement."""

        self. eating ()
        self. prey_spawn ()
        self. predator_death ()

    def turn_no_movement_and_randomise_placement (self):

        self. turn_no_movement ()
        self. randomise_placements ()
    
    def move  (self):
        """Moves the animals on the grid."""

        chance_of_moving = 0.5

        new_grid = create_empty_grid (col_num = self. col_num, row_num = self. row_num)

        for r, row in enumerate(self. grid):
            for c, point in enumerate(row):
                for i in range (2):
                    for _ in range (point [i]):
                        if not(self. rng. random () < chance_of_moving):
                            # Animal stays still
                            new_grid[r][c][i] += 1
                            continue

                        move = self. rng. choice (['down', 'left', 'right', 'up'])

                        vert_mov = 0
                        horiz_mov = 0

                        if move == 'down':
                            horiz_mov = 0
                            vert_mov = 1
                        elif move == 'left':
                            horiz_mov = -1
                            vert_mov = 0
                        elif move == 'up':
                            horiz_mov = 0
                            vert_mov = -1
                        elif move == 'right':
                            horiz_mov = 1
                            vert_mov = 0

                        if 0 <= r + vert_mov <= self. row_num - 1 and 0 <= c + horiz_mov <= self. col_num -1:
                            new_row = r + vert_mov
                            new_column = c + horiz_mov

                        else:
                            new_row, new_column = self. edge_function (r, c)

                        new_grid [new_row] [new_column] [i] += 1

        self. grid = new_grid

    def move_no_escape (self, r, c):
        """For when an animal walks off the grid. Returns its current point, not allowing the animal to escape the grid."""

        return r, c

    def move_im_em (self, r, c):
        """(Immigration, Emmigration on the edge) For when an animal walks off the grid. It gives a random point on the edge of the grid for the animal to be transported to."""

        draw = self. rng. integers (low = 0, high = (self. row_num + self. col_num) * 2) # - 4 for corners and + 4 for recounting corners

        if draw < self. row_num:
            new_column = 0
            new_row = draw
        
        elif draw < self. row_num + self. col_num - 1:
            new_column = draw - (self. row_num - 1)
            new_row = self. row_num - 1

        elif draw < self. row_num * 2 + self. col_num - 2:
            new_column = self. col_num - 1
            new_row = 2 * (self. row_num - 1) + (self. col_num - 1) - draw

        elif draw < self. row_num * 2 + self. col_num * 2 - 4:
            new_column = (self. row_num - 1) * 2 + (self. col_num - 1) * 2 - draw
            new_row = 0

        # giving corners an extra chance to be landed on
        elif draw == self. row_num * 2 + self. col_num * 2 - 4:
            new_column = 0
            new_row = 0

        elif draw == self. row_num * 2 + self. col_num * 2 - 3:
            new_column = 0
            new_row = self. row_num - 1

        elif draw == self. row_num * 2 + self. col_num * 2 - 2:
            new_column = self. col_num - 1
            new_row = self. row_num - 1

        else:
            new_column = self. col_num - 1
            new_row = 0

        return new_row, new_column

    def eating (self):
        """Conducts eating on the grid."""

        for r, row in enumerate(self. grid):

            for c, point in enumerate(row):

                if point [0] > 0 and point [1] > 0:

                    self. pred_reproduction_function (r, c)


    def predator_spawns_whether_or_not_prey_die (self, row, column):
        """Handling predator spawning and prey death at a given grid point defined by row and column. Predator reproduction does not depend on prey death."""

        num_preds = self. grid [row] [column] [1]

        num_prey_left = self. grid [row] [column] [0]

        for _ in range(num_preds):

            for _ in range(num_prey_left):

                # Chance that prey dies
                if self. rng. random () < self. a:
                    self. grid [row] [column] [0] -= 1
                    num_prey_left -= 1

                # Chance that extra predator spawns
                if self. rng. random () < self. b:
                    self. grid [row] [column] [1] += 1

    def predator_spawns_only_if_prey_dies (self, row, column):
        """Handling predator spawning and prey death at a given grid point defined by row and column. Predator reproduction only happens if a prey dies."""
        
        num_preds = self. grid [row] [column] [1]

        num_prey_left = self. grid [row] [column] [0]

        for _ in range(num_preds):

            for _ in range(num_prey_left):

                # Chance that prey dies
                if self. rng. random () < self. a:
                    self. grid [row] [column] [0] -= 1
                    num_prey_left -= 1

                    # Chance that extra predator spawns
                    if self. rng. random () < self. b:
                        self. grid [row] [column] [1] += 1
    
    def count_pairs (self):
        """Counts prey-predator pairs."""

        num_prey_predator_pairs = 0

        for r, row in enumerate(self. grid):
            for c, point in enumerate(row):

                num_prey_predator_pairs += point [0] * point [1]
            
        return num_prey_predator_pairs

    
    def prey_spawn(self):
        """Conducts prey reproduction on the grid."""

        for row_index, row in enumerate(self. grid):

            for col_index, point in enumerate(row):

                num_prey = point [0]

                for _ in range (point [0] ):
                    if self. rng. random() < self. c:
                        num_prey += 1
        
                self. grid [row_index] [col_index] [0] = num_prey

    def predator_death(self):
        """Conducts predator death on the grid."""
        
        for row_index, row in enumerate(self. grid):
            for col_index, point in enumerate(row):

                num_preds_left_alive = point [1]

                for _ in range (point [1] ):

                    if self. rng. random () < self. d:
                        num_preds_left_alive -= 1
                
                self. grid [row_index] [col_index] [1] = num_preds_left_alive

    def stats_count(self):
        """Count up number of preys, predators, and prey-predator pairs."""

        prey_count = 0
        predator_count = 0
        num_prey_predator_pairs = 0

        for row in self. grid:
            for point in row:
                prey_count += point [0]
                predator_count += point [1]
                num_prey_predator_pairs += point [0] * point [1]

        
        return prey_count, predator_count, num_prey_predator_pairs
    
    def print_grid(self):
        print('----Outputting grid----')
        for row in self.grid:
            print(row) 

    def create_grid (self):

        grid = create_empty_grid (self. col_num, self. row_num)

        grid = randomly_place_animals (
            num_prey = self. init_prey,
            num_pred = self. init_pred,
            grid = grid,
            col_num = self. col_num,
            row_num = self. row_num,
            rng = self. rng,
        )

        return grid
    
    def randomise_placements (self):

        num_prey, num_preds, _ = self. stats_count ()

        self. empty_grid ()

        self. grid = randomly_place_animals (
            num_prey = num_prey,
            num_pred = num_preds,
            grid = self. grid,
            col_num = self. col_num,
            row_num = self. row_num,
            rng = self. rng,
        )

    
    def empty_grid (self):

        for row in self.grid:
          
            for point in row:

                point [:] = (0, 0)



def create_empty_grid (col_num, row_num):

    return np. zeros ( (row_num, col_num, 2), dtype = int) . tolist ()


def randomly_place_animals (
        num_prey: int,
        num_pred: int,
        grid: list,
        col_num: int,
        row_num: int,
        rng: Generator
):
    """Randomly place the given number of animals onto the grid."""

    random_numbers = rng. integers (low = 0, high = col_num * row_num, size = num_pred + num_prey)
    
    for i in range (num_pred):

        rn = random_numbers [i]

        # row then col
        grid [rn // col_num] [rn % col_num] [1] += 1

    for i in range (num_pred, num_pred + num_prey):
        rn = random_numbers [i]

        grid [rn // col_num] [rn % col_num] [0] += 1

    return grid