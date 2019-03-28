from tkinter import *
import numpy as np





def checkered(canvas, line_distance, canvas_height, canvas_width):
   # vertical lines at an interval of "line_distance" pixel
   for x in range(line_distance,canvas_width,line_distance):
      canvas.create_line(x, 0, x, canvas_height, fill="#476042")
   # horizontal lines at an interval of "line_distance" pixel
   for y in range(line_distance,canvas_height,line_distance):
      canvas.create_line(0, y, canvas_width, y, fill="#476042")




def update_grid_state_value_function(grid_values_old, GRID_DIM, trans_prob, REWARD, DISCOUNT_FACTOR):
    v_fn = 0

    # Initialise new matrix to store updated state value function
    grid_values_new = np.zeros([GRID_DIM,GRID_DIM])
    grid_values_new = np.pad(grid_values_new, ((1, 1), (1, 1)), mode='constant', constant_values=0)

    for i in range(1, grid_values_old.shape[0]-1):
        for j in range(1, grid_values_old.shape[1] - 1):
            v_fn += trans_prob["UP"]*(REWARD + DISCOUNT_FACTOR * grid_values_old[i+1,j])
            v_fn += trans_prob["DOWN"] * (REWARD + DISCOUNT_FACTOR * grid_values_old[i-1, j])
            v_fn += trans_prob["LEFT"] * (REWARD + DISCOUNT_FACTOR * grid_values_old[i, j-1])
            v_fn += trans_prob["RIGHT"] * (REWARD + DISCOUNT_FACTOR * grid_values_old[i, j+1])

            grid_values_new[i,j] = v_fn
            v_fn = 0
    return grid_values_new




def reset_state_values(grid_values):
    num_rows = grid_values.shape[0]
    num_cols = grid_values.shape[1]
    # Update first row padded
    grid_values[0] = grid_values[1]
    # Update bottom row padded
    grid_values[num_rows-1] = grid_values[num_rows-2]
    # Update left column padded values
    grid_values[:,0] = grid_values[:,1]
    # Update right column padded values
    grid_values[:,num_cols-1] = grid_values[:,num_cols-2]

    return grid_values





def reset_goal_values(grid_values, goals_dim):
    for goal in goals_dim:
        grid_values[goal[0],goal[1]] = 0
    return grid_values




def print_unpadded_matrix(value_matrix, GRID_DIM):
    return value_matrix[1:GRID_DIM+1,1:GRID_DIM+1]




def pretty_print_matrix(value_matrix, CANVAS_HEIGHT_WIDTH, GRID_DIM, label_offset, line_distance):
    master = Tk()
    canvas_width = CANVAS_HEIGHT_WIDTH
    canvas_height = CANVAS_HEIGHT_WIDTH
    w = Canvas(master,
               width=canvas_width,
               height=canvas_height)
    w.pack()

    for j in range(GRID_DIM):
        for i in range(GRID_DIM):
            w.create_text(label_offset + i * line_distance, label_offset + j * line_distance, fill="darkblue",
                          font="Times 20 italic bold",
                          text=str(value_matrix[j+1,i+1]))
    return [w, canvas_height, canvas_width]