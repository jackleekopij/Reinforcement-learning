from tkinter import *
import numpy as np
from dynamic_programming_helpers import *


CANVAS_HEIGHT_WIDTH = 600
GRID_DIM = 4
np.set_printoptions(suppress=True)

DISCOUNT_FACTOR = 1.0
REWARD = -1

line_distance = CANVAS_HEIGHT_WIDTH/GRID_DIM
label_offset = line_distance/2


#### Define policy
trans_prob = {"UP":0.25, "DOWN":0.25, "LEFT":0.25, "RIGHT":0.25}









# Initialise state value function
grid_values = np.zeros([GRID_DIM,GRID_DIM])
# Add edge of padding to simulate an edge node returning to state
grid_values = np.pad(grid_values,((1,1),(1,1)), mode='constant', constant_values=0)


grid_values = reset_goal_values(grid_values, goals_dim=[[1,1],[5,5]])





'''
ITERATE AND UPDATE VALUE FUNCTION ONE ITERATION AT A TIME - UPDATING VALUE FUNCTION FOR EACH STATE.
'''
updated_grid_value = update_grid_state_value_function(grid_values, GRID_DIM, trans_prob, REWARD, DISCOUNT_FACTOR).round(2)
print(updated_grid_value)
print("\n")
updated_grid_value = reset_state_values(updated_grid_value).round(2)
print(reset_state_values(updated_grid_value).round(2))
print("\n")
updated_grid_value = reset_goal_values(updated_grid_value, goals_dim=[[1,1],[5,5]]).round(2)
print(updated_grid_value)



print("[IN] next iteration of code")
updated_grid_value = update_grid_state_value_function(updated_grid_value, GRID_DIM, trans_prob, REWARD, DISCOUNT_FACTOR).round(2)
print(updated_grid_value)
print("\n")
updated_grid_value = reset_state_values(updated_grid_value).round(2)
print(reset_state_values(updated_grid_value).round(2))
print("\n")
updated_grid_value = reset_goal_values(updated_grid_value, goals_dim=[[1,1],[5,5]]).round(2)
print(updated_grid_value)

print("[IN] next iteration of code")
updated_grid_value = update_grid_state_value_function(updated_grid_value, GRID_DIM, trans_prob, REWARD, DISCOUNT_FACTOR).round(2)
print(updated_grid_value)
print("\n")
updated_grid_value = reset_state_values(updated_grid_value).round(2)
print(reset_state_values(updated_grid_value).round(2))
print("\n")
updated_grid_value = reset_goal_values(updated_grid_value, goals_dim=[[1,1],[5,5]]).round(2)
print(updated_grid_value)



w,canvas_height,canvas_width = pretty_print_matrix(updated_grid_value, CANVAS_HEIGHT_WIDTH, GRID_DIM, label_offset, line_distance)
checkered(w, line_distance, canvas_height, canvas_width)
mainloop()