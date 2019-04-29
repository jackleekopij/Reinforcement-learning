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
NUM_EPISODES = 100



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

    def boundary_state_check(self, current_state):
        '''
        boundary_state_check constrains the agent to eligible moves by constraining moves that would otherwise have the agent
        transition outside of the boundary.
        :param dims: the dimensions of the windy world board.
        :return: a state vector after boundary analysis of the agent.
        '''
        # calc the horizontal boundaries of the windy world board
        current_state[0] = min(current_state[0], self.board_dim[0]-1)
        current_state[0] = max(current_state[0], 0)

        # calc the vertical boundaries of the windy world board
        current_state[1] = min(current_state[1], self.board_dim[1]-1)
        current_state[1] = max(current_state[1], 0)
        return current_state

    def update_state(self, agent_action, prev_state):
        '''
        Return a vector of the agents state after taking a move in the environment
        :param agent_action: a 2d list to add to the previous state.
        :param prev_state: a 2d list of the previous state.
        :return: updated state to without the environments wind effect
        '''
        current_col = prev_state[0] + agent_action[0]
        current_col_wind_effect = self.wind_vector[current_col]
        current_state = [current_col, prev_state[1] + current_col_wind_effect + agent_action[1]]
        current_state = self.boundary_state_check(current_state)
        print("Current state: {}".format(current_state))
        return current_state

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
'''
class SARSA_agent():
    def __init__(self):
    def
'''



# main function
if __name__ == "__main__":
    # Create wind_env object
    # TODO: create gym enovironmen for windy world for reuse
    wind_env = wind_world(wind_vector=[0,0,0,1,1,1,2,2,1,0], board_dim=[7,10], start_state=[0,0], goal_state=[5,8])


    # Training loop:
    for i in range(NUM_EPISODES):
        wind_env.update_state([-1,-1], [0,0])
        break
        i += 1

        # Create function to calculate Q
        # A 70 by 4 matrix

        
    # Training output: