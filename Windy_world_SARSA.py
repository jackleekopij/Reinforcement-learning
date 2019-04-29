import pandas as pd
import numpy as np
from random import randint

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
EPSILON = 0.05
NUM_EPISODES = 100
BOARD_DIM = [7,10]
INIT_STATE = [3,0]
GOAL_STATE = [5,8]
# ACTIONS = {"UP":[0,1], "DOWN":[0,-1], "LEFT":[-1,0], "RIGHT":[]}
ACTIONS = [[0,1], [0,-1], [-1,0], [1,0]]





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

    def next_state(self, agent_action, prev_state):
        '''
        Return a vector of the agents state after taking a move in the environment
        :param agent_action: a 2d list to add to the previous state.
        :param prev_state: a 2d list of the previous state.
        :return: updated state to without the environments wind effect
        '''
        current_col = prev_state[1] + agent_action[1]
        current_row_wind_effect = self.wind_vector[current_col]
        current_state = [prev_state[0] + current_row_wind_effect + agent_action[0], current_col]
        current_state = self.boundary_state_check(current_state)
        return current_state


def calc_reward(current_state, GOAL_STATE):
    '''
    Function to calculate the returns for environment. Penalise if the agent doesn't transition into the goal state
    :return:
    '''
    if current_state == GOAL_STATE:
        return 100
    else:
        return 0




# SARSA agent function
# Create a SARSA policy agent with an epsilon greedy algorithm.
def SARSA_agent(wind_env, Qmatrix, current_state, goal_state, ACTIONS, ALPHA, EPSILON, GAMMA, GOAL_STATE):
    # One step look ahead
    unraveled_current_state = np.ravel_multi_index(current_state,BOARD_DIM)
    action = egreedy_action(Qmatrix, unraveled_current_state, EPSILON)
    # Two step look ahead
    reward = calc_reward(current_state,GOAL_STATE)

    state_prime = wind_env.next_state(ACTIONS[action], current_state)
    unraveled_prime_state = np.ravel_multi_index(state_prime,BOARD_DIM)
    prime_action = egreedy_action(Qmatrix, unraveled_prime_state, EPSILON)

    Qmatrix[unraveled_current_state][action] +=   ALPHA*(reward + GAMMA*Qmatrix[unraveled_prime_state][prime_action] - Qmatrix[unraveled_current_state][action])

    return Qmatrix




def egreedy_action(Qmatrix, state,EPSILON):
    if (np.random.rand < EPSILON):
        action = randint(0, 3)
    else:
        action = np.argmax(Qmatrix[state])





# main function
if __name__ == "__main__":
    # Create wind_env object
    # TODO: create gym enovironment for windy world for reuse.
    # Added additional wind value as a buffer for agent sampling states above 10
    wind_env = wind_world(wind_vector=[0,0,0,1,1,1,2,2,1,0,0], board_dim=BOARD_DIM, start_state=[0,0], goal_state=GOAL_STATE)

    # Initialise Q-matrix
    num_states = BOARD_DIM[0] * BOARD_DIM[1]
    num_actions = len(ACTIONS)
    Qmatrix = np.zeros([num_states,num_actions])

    current_state = INIT_STATE

    # Training loop:
    for i in range(NUM_EPISODES):
        print("Current state pre update: {}".format(current_state))
        current_state = wind_env.next_state(ACTIONS[0], current_state)

        print("Current state post update: {}".format(current_state))
        print(i)

        if i > 10:
            break

        i += 1

        # Create function to calculate Q
        # A 70 by 4 matrix

    # Calculate row of Q matrix to update
    print("index of q-matrix: {}".format(np.ravel_multi_index(current_state,BOARD_DIM)))


    # Training output: