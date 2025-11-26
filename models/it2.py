'''
The first iteration does not follow Lotka-Volterra exactly because it does not simulate unlimited hunger by predators.
Iteration two tries to get closer to this notion
'''


import random as rd
import copy

# Parameters
a = 0.8 # Probability that if a prey gets paired with a predator, it will die
b = 0.1 # Probability that if a predator gets paired with a prey, it will reproduce
c = 0.01 # Probability that a prey will reproduce
d = 0 # Probability of death for a predator

# Number of turns
num_turns = 1000

# Define grid as n by n grid of empty lists
col_num = row_num = 20
grid = [[[] for _ in range(col_num)] for _ in range(row_num)]

# Add initial animals
initial_num_predators = 60
initial_num_prey = 100

def put_into_rd_grid_space(object, row_num, col_num, grid):
    random_row = rd.randint(0, row_num - 1)
    random_column = rd.randint(0, col_num - 1)
    grid[random_row][random_column].append(object)
    return grid

for _ in range(initial_num_predators):
    # random 0 to 9 * 2 and put into that grid space
    grid = put_into_rd_grid_space('pred', row_num, col_num, grid)

for _ in range(initial_num_prey):
    grid = put_into_rd_grid_space('prey', row_num, col_num, grid)

# Define movement
def move(grid, row_num, col_num):
    new_grid = [[[] for _ in range(col_num)] for _ in range(row_num)]

    for r, row in enumerate(grid):
        for c, point in enumerate(row):
            for animal in point:
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
def eating(grid):
    for r, row in enumerate(grid):
        for c, point in enumerate(row):
            prey_list = []
            predator_list = []

            for i, animal in enumerate(point):
                if animal == 'prey':
                    prey_list.append(i)
                else:
                    predator_list.append(i)

            # If there is an animal at the point, then iterate over the number of prey, finding out each time whether a prey dies and a new predator comes alive
            if len(predator_list) > 0:
                for i in range(len(prey_list)):
                    # Chance that prey dies
                    if rd.random() < a:
                        grid[r][c].remove('prey')

                    # Chance that extra predator spawns
                    if rd.random() < b:
                        grid[r][c].append('pred')
    return grid

# prey reproduction
def prey_spawn(grid):
    new_grid = copy.deepcopy(grid)
    for row_index, row in enumerate(grid):
        for col_index, point in enumerate(row):
            for animal in point:
                if animal == 'prey':
                    if rd.random() < c:
                        new_grid[row_index][col_index].append('prey')
    
    return new_grid

# predator death
def predator_death(grid):
    new_grid = copy.deepcopy(grid)
    for row_index, row in enumerate(grid):
        for col_index, point in enumerate(row):
            for animal in point:
                if animal == 'pred':
                    if rd.random() < d:
                        new_grid[row_index][col_index].remove('pred')
    
    return new_grid


def counting(grid):
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


# Printing grid
def print_grid(grid):
    print('----Outputting grid----')
    for row in grid:
        print(row)


# Run experiment and output to dat file
def out_to_dat(file_name, grid, initial_num_prey, initial_num_predators, row_num, col_num, num_turns):
    with open(file_name, 'w') as file:
        file.write(f'0 {initial_num_prey} {initial_num_predators}')
        
        prey_count = 0
        for i in range(num_turns):

            # Stop exponential growth
            if prey_count > 100 * initial_num_prey:
                return
            
            turn = i + 1
            grid = move(grid, row_num, col_num)
            grid = eating(grid)
            grid = prey_spawn(grid)
            grid = predator_death(grid)
            prey_count, predator_count = counting(grid)
            file.write(f'\n{turn} {prey_count} {predator_count}')


# Run experiment with standard out
def out_to_std(grid, initial_num_prey, initial_num_predators, row_num, col_num, num_turns):
    print(f'Initial, Prey count: {initial_num_prey}, Predator count: {initial_num_predators}')

    for i in range(num_turns):
        turn = i + 1
        grid = move(grid, row_num, col_num)
        grid = eating(grid)
        grid = prey_spawn(grid)
        grid = predator_death(grid)
        prey_count, predator_count = counting(grid)
        print(f'Turn: {turn}, Prey count: {prey_count}, Predator count: {predator_count}')



# out_to_std(grid, initial_num_prey, initial_num_predators, row_num, col_num, num_turns)

file_name = 'data/test.dat'
out_to_dat(file_name, grid, initial_num_prey, initial_num_predators, row_num, col_num, num_turns)
