from tkinter import *
import numpy as np

CANVAS_HEIGHT_WIDTH = 600
GRID_DIM = 5
np.set_printoptions(suppress=True)

DISCOUNT_FACTOR = 1.0
REWARD = -1

line_distance = CANVAS_HEIGHT_WIDTH/GRID_DIM
label_offset = line_distance/2


#### Define policy
trans_prob = {"UP":0.25, "DOWN":0.25, "LEFT":0.25, "RIGHT":0.25}



def checkered(canvas, line_distance):
   # vertical lines at an interval of "line_distance" pixel
   for x in range(line_distance,canvas_width,line_distance):
      canvas.create_line(x, 0, x, canvas_height, fill="#476042")
   # horizontal lines at an interval of "line_distance" pixel
   for y in range(line_distance,canvas_height,line_distance):
      canvas.create_line(0, y, canvas_width, y, fill="#476042")



master = Tk()
canvas_width = CANVAS_HEIGHT_WIDTH
canvas_height = CANVAS_HEIGHT_WIDTH
w = Canvas(master,
           width=canvas_width,
           height=canvas_height)
w.pack()

for i in range(GRID_DIM):
    w.create_text(label_offset + i * line_distance, label_offset,fill="darkblue",font="Times 20 italic bold",
                        text="0.0")

# Initialise state value function
grid_values = np.zeros([GRID_DIM,GRID_DIM])
# Add edge of padding to simulate an edge node returning to state
grid_values = np.pad(grid_values,((1,1),(1,1)), mode='constant', constant_values=0)

print(grid_values)


#
'''

def padded_grid_iterate(grid_values):
    for i in range(1, grid_values.shape[0]-1):
        for j in range(1, grid_values.shape[1] - 1):
            print(grid_values[j][i])


padded_grid_iterate(grid_values)

'''

def update_grid_state_value_function(grid_values_old, GRID_DIM):
    v_fn = 0

    # Initialise new matrix to store updated state value function
    grid_values_new = np.zeros([GRID_DIM,GRID_DIM])
    grid_values_new = np.pad(grid_values_new, ((1, 1), (1, 1)), mode='constant', constant_values=0)

    for i in range(1, grid_values_old.shape[0]-1):
        for j in range(1, grid_values_old.shape[1] - 1):
            print("[IN] column number {} ".format(i))
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


grid_values = reset_goal_values(grid_values, goals_dim=[[1,1],[5,5]])


updated_grid_value = update_grid_state_value_function(grid_values, GRID_DIM).round(2)
print(updated_grid_value)
print("\n")
updated_grid_value = reset_state_values(updated_grid_value).round(2)
print(reset_state_values(updated_grid_value).round(2))
print("\n")
updated_grid_value = reset_goal_values(updated_grid_value, goals_dim=[[1,1],[5,5]]).round(2)
print(updated_grid_value)
checkered(w,line_distance)

print("[IN] next iteration of code")
updated_grid_value = update_grid_state_value_function(updated_grid_value, GRID_DIM).round(2)
print(updated_grid_value)
print("\n")
updated_grid_value = reset_state_values(updated_grid_value).round(2)
print(reset_state_values(updated_grid_value).round(2))
print("\n")
updated_grid_value = reset_goal_values(updated_grid_value, goals_dim=[[1,1],[5,5]]).round(2)
print(updated_grid_value)

mainloop()