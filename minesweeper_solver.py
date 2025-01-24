import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np
import random

def fetch_subgrid(arr, index_tuple):
    row, col = index_tuple
    y1, y2 = row-1, row+2
    x1, x2 = col-1, col+2
    if y1 < 0: y1 = 0
    if x1 < 0: x1 = 0
    return arr[y1:y2, x1:x2]

def generate_fields(field_shape=(30, 40), mine_count = 80):
    fsize = field_shape[0] * field_shape[1]
    listed_field_addresses = list(range(fsize))
    mine_locations = random.sample(listed_field_addresses, k=mine_count)
    
    field = fsize * [0]
    
    for mine_index in mine_locations:
        field[mine_index] = 1
    
    mine_field = np.array(field)
    
    mine_field = mine_field.reshape(field_shape)
    
    game_field = np.zeros_like(mine_field)
    
    index_list = []
    for index, _ in np.ndenumerate(game_field):
        index_list.append(index)
    
    index_array = np.array(index_list).reshape((field_shape[0], field_shape[1], 2))
    
    for row in range(field_shape[0]):
        for col in range(field_shape[1]):
            if mine_field[row, col] == 1:
                game_field[row, col] = 9
            else:
                y1, y2 = row-1, row+2
                x1, x2 = col-1, col+2
                
                if y1 < 0: 
                    y1 = 0
    
                if x1 < 0: 
                    x1 = 0
                
                game_field[row, col] = mine_field[y1:y2, x1:x2].sum()

    starting_choices = []
    for index, val in np.ndenumerate(game_field):
        if val == 0:
            starting_choices.append(index)
    
    starting_pos = random.choice(starting_choices)
    
    solution_field = np.zeros_like(game_field) + 10

    return solution_field, starting_pos, game_field, mine_field, index_array


def solve_grid(solution_field, starting_pos, game_field, index_array, all_frames):
    queue = []
    already_revealed = set([])
    hidden_mines = set([])
    # add starting position
    queue.append(starting_pos)
    
    while any(queue):
        
        reveal_index = queue.pop(0)
        already_revealed.add(reveal_index)
        
        row, col = reveal_index
        y1, y2 = row-1, row+2
        x1, x2 = col-1, col+2
        if y1 < 0: y1 = 0
        if x1 < 0: x1 = 0
    
        #reveal
        solution_field[y1:y2, x1:x2] = game_field[y1:y2, x1:x2]
        
        all_frames.append(solution_field.copy())
    
        # we use this to add the original indexes and not the subset slice array indexes
        for original_index in index_array[y1:y2, x1:x2].reshape(-1, 2):
            index_tuple = tuple([int(i) for i in original_index])
            number_hint = solution_field[index_tuple]
            # check if number == 0 or number - count(9) == 0
            if number_hint == 0 and index_tuple not in queue and index_tuple not in already_revealed:
                queue.append(tuple([int(i) for i in original_index]))
            elif number_hint < 9:
                grid_around_hint = fetch_subgrid(solution_field, index_tuple)
                indices_around_hint = fetch_subgrid(index_array, index_tuple)
                if np.count_nonzero(grid_around_hint == 10) == number_hint - np.count_nonzero(grid_around_hint == 9):
                    # mark mines
                    for i, val in enumerate(grid_around_hint.flatten()):
                        if val == 10:
                            index_of_mine = tuple([int(i) for i in indices_around_hint.reshape(-1, 2)[i]])
                            hidden_mines.add(index_of_mine)
                            solution_field[index_of_mine] = 9
                    # TODO: after mines are added we should make sure not to reveal this later                                 <<<< TODO:
                    # for now we add this to be revealed to the queue
                    if index_tuple not in already_revealed:
                        queue.append(index_tuple)
                if number_hint == np.count_nonzero(grid_around_hint == 9) and index_tuple not in already_revealed and index_tuple not in queue:
                    queue.append(index_tuple)
    
    return solution_field, hidden_mines, already_revealed, all_frames

def animate_solution(mine_count = 60, field_shape = (16, 30)):
    
    all_frames = []

    solution_field, starting_pos, game_field, mine_field, index_array = generate_fields(field_shape=field_shape, mine_count = mine_count)

    all_frames.append(solution_field.copy())

    solution_field, hidden_mines, already_revealed, all_frames = solve_grid(solution_field=solution_field, starting_pos=starting_pos, game_field=game_field, index_array=index_array, all_frames=all_frames)
        

    print(f'mines: {len(hidden_mines)}/{mine_count}, spaces: {len(already_revealed)}/{field_shape[0]*field_shape[1]} iterations: {len(all_frames)}')

    def update(data):
        mat.set_data(data)
        return mat

    fig, ax = plt.subplots()
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    mat = ax.matshow(all_frames[0], cmap='viridis', vmin=0, vmax=10, animated=True)

    ani = animation.FuncAnimation(fig, 
                                update, 
                                all_frames, 
                                interval=40,
                                repeat_delay=1000
                                #save_count=50,
                                )
    return ani
