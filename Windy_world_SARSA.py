import pandas as pd
import numpy as np

# Windy-world is an environment of discrete states (the example used will be a the classic 7x10 grid).
# For each of the columns there is a 'wind' that pushes the agent up by a varying magnitude.
# The wind effect column vector is represented as [0,0,0,1,1,1,2,2,1,0]


'''
Environment notes: 
    Windy environment is an extension of grid world with a discrete state space. In this application the bottom left 
    corner is set to the origin, (0,0). 
'''


# SET PARAMETERS
GRID_DIM = [7,10]
QMATRIX = np.zeros(GRID_DIM)






# Create environment (wind world)
class wind_world():
    '''
    Create a windy_world board.
    '''
    def __init__(self, wind_vector,board_dim, start_state, goal_state):
        self.wind_vector = wind_vector
        self.board_dim = board_dim
        self.current_state = start_state
        self.goal = goal_state
        print("The board dimension is: {}".format(board_dim))


    def update_state(self, agent_action, prev_state, wind_vector):
        '''
        Return a vector of the agents state after taking a move in the environment
        :param agent_action: a 2d list to add to the previous state.
        :param prev_state: a 2d list of the previous state.
        :return: updated state to without the environments wind effect
        '''
        current_col = prev_state[0] + agent_action[0]
        current_col_wind_effect = wind_vector[current_col]
        return [current_col, prev_state[1] + current_col_wind_effect + agent_action[1]]

    def calc_reward(self):
        '''
        Function to calculate the returns for environment. Penalise if the agent doesn't transition into the goal state
        :return:
        '''
        if self.current_state == self.goal_state:
            return 100
        else:
            return -1

# SARSA agent function
class SARSA_agent():
    def __init__(self):
    def

# main function
if __name__ == "__main__":
    wind_env = wind_world(wind_vector=[2,3], board_dim=[4,5], start_state=[0,0])
    print(wind_en)