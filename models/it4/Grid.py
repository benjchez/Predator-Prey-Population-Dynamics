import random as rd
import copy

from AnimalParameters import AnimalParameters
from GraphOptions import GraphOptions

class Grid:
    def __init__(self, o: GraphOptions, p: AnimalParameters):
        self.grid = create_grid(o.col_num, o.row_num, o.init_num_pred, o.init_num_prey)
        self.init_prey = o.init_num_prey
        self.init_pred = o.init_num_pred
        self.col_num = o.col_num
        self.row_num = o.row_num
        self.a = p.a
        self.b = p.b
        self.c = p.c
        self.d = p.d

    def turn(self):
        self.move()
        self.eating()
        self.prey_spawn()
        self.predator_death()

    
    def move(self):
        self.grid = move(self.grid, self.row_num, self.col_num)

    def eating(self):
        self.grid = eating(self.grid, self.a, self.b)
    
    def prey_spawn(self):
        self.grid = prey_spawn(self.grid, self.c)
    
    def predator_death(self):
        self.grid = predator_death(self.grid, self.d)

    def an_count(self):
        return an_count(self.grid)
    
    # Printing grid
    def print_grid(self):
        print('----Outputting grid----')
        for row in self.grid:
            print(row)
    

    


def put_into_rd_grid_space(object, row_num, col_num, grid):
    random_row = rd.randint(0, row_num - 1)
    random_column = rd.randint(0, col_num - 1)
    grid[random_row][random_column].append(object)
    return grid

def create_grid(col_num, row_num, initial_num_predators, initial_num_prey):
    grid = [[[] for _ in range(col_num)] for _ in range(row_num)]
    for _ in range(initial_num_predators):
        # random 0 to 9 * 2 and put into that grid space
        grid = put_into_rd_grid_space('pred', row_num, col_num, grid)

    for _ in range(initial_num_prey):
        grid = put_into_rd_grid_space('prey', row_num, col_num, grid)
    
    return grid


# Define movement
def move(grid, row_num, col_num):
    chance_of_moving = 0.5

    new_grid = [[[] for _ in range(col_num)] for _ in range(row_num)]

    for r, row in enumerate(grid):
        for c, point in enumerate(row):
            for animal in point:
                if not(rd.random() < chance_of_moving):
                    # Animal stays still
                    new_grid[r][c].append(animal)
                    continue

                move = rd.choice(['down', 'left', 'right', 'up'])

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

                if 0 <= r + vert_mov <= row_num - 1:
                    new_row = r + vert_mov
                else:
                    new_row = r
                if 0 <= c + horiz_mov <= col_num -1:
                    new_column = c + horiz_mov
                else:
                    new_column = c
                new_grid[new_row][new_column].append(animal)
    return new_grid

# Define eating mechanism
def eating(grid, a, b):
    for r, row in enumerate(grid):
        for c, point in enumerate(row):
            prey_list = []
            predator_list = []

            for i, animal in enumerate(point):
                if animal == 'prey':
                    prey_list.append(i)
                else:
                    predator_list.append(i)

            # Iterate over each predator in the grid space. For each predator, iterate over the number of prey left alive in the grid space. If a prey dies then the subsequent predators do not get a chance to eat it (which is why we decrement num_prey_left).
            if len(predator_list) > 0:

                num_prey_left = len(prey_list)

                for _ in range(len(predator_list)):

                    for _ in range(num_prey_left):

                        # Chance that prey dies
                        if rd.random() < a:
                            grid[r][c].remove('prey')
                            num_prey_left -= 1

                        # Chance that extra predator spawns
                        if rd.random() < b:
                            grid[r][c].append('pred')
    return grid

# prey reproduction
def prey_spawn(grid, c):
    new_grid = copy.deepcopy(grid)
    for row_index, row in enumerate(grid):
        for col_index, point in enumerate(row):
            for animal in point:
                if animal == 'prey':
                    if rd.random() < c:
                        new_grid[row_index][col_index].append('prey')
    
    return new_grid

# predator death
def predator_death(grid, d):
    new_grid = copy.deepcopy(grid)
    for row_index, row in enumerate(grid):
        for col_index, point in enumerate(row):
            for animal in point:
                if animal == 'pred':
                    if rd.random() < d:
                        new_grid[row_index][col_index].remove('pred')
    
    return new_grid

def an_count(grid):
    prey_count = 0
    predator_count = 0

    for row in grid:
        for point in row:
            for animal in point:
                if animal == 'prey':
                    prey_count += 1
                else:
                    predator_count += 1
    
    return prey_count, predator_count

