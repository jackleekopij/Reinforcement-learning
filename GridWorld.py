import numpy as np
from helpers_qlearning import *
import matplotlib.pyplot as plt
#---------------------#
# TODO
#    Set R matrix, the reward matrix to a value of 5 if reach the goal
#    Initialize the Q matrix to zero
#    Get available actions
#    Select action
#    Update the Q matrix
#    G
#
#
#
#----------------------#

supress_print = False
dimensions= [3,3]
q_dims = dimensions[0] * dimensions[1]


# R matrix
R = np.matrix([[-1, -1, -1, -1, 0, -1],
               [-1, -1, -1, 0, -1, 100],
               [-1, -1, -1, 0, -1, -1],
               [-1, 0, 0, -1, 0, -1],
               [-1, 0, 0, -1, -1, 100],
               [-1, 0, -1, -1, 0, 100]])
#R = create_reward_matrix(dimensions, [[1,0], [2,1]], [2,2], 50 )

R = np.matrix([[-1,0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[0, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[-1, 0, -1, -0, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[-1, -1, 0, -1, -1, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1],
[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[-1, -1, 0, -1, -1, -1, -1, 0, -1, -1, 0, -1, -1, -1, -1, -1],
[-1, -1, -1, 0, -1, -1, 0, -1, -1, -1, -1, 0, -1, -1, -1, -1],
[-1, -1, -1, -1, -1, -1, -1, -1, -1, 0, -1, -1, 0, -1, -1, -1],
[-1, -1, -1, -1, -1, -1, -1, -1, 0, -1, 0, -1, -1, 0, -1, -1],
[-1, -1, -1, -1, -1, -1, 0, -1, -1, 0, -1, 0, -1, -1, 0, -1],
[-1, -1, -1, -1, -1, -1, -1, 0, -1, -1, 0, -1, -1, -1, -1, 100],
[-1, -1, -1, -1, -1, -1, -1, -1, 0, -1, -1, -1, -1, 0, -1, -1],
[-1, -1, -1, -1, -1, -1, -1, -1, -1, 0, -1, -1, 0, -1, 0, -1],
[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, -1, -1, 0, -1, 100],
[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 100]])
# Q matrix
Q = np.matrix(np.zeros([16, 16]))

# Gamma (learning parameter).
gamma = 0.8

# Initial state. (Usually to be chosen at random)
initial_state = 1


# This function returns all available actions in the state given as an argument
def available_actions(state):
    current_state_row = R[state,]
    if not supress_print:
        print("Current state row {0}".format(current_state_row))
        print("Average action to be used {0}".format(np.where(current_state_row >= 0)))
    # Available actions will ensure the agent cannot move through walls etc.
    # since walls have a negative reward.
        print("The current state {0}".format(np.where(current_state_row >=0)[0]))
    av_act = np.where(current_state_row >= 0)[1]
    return av_act


# Get available actions in the current state
available_act = available_actions(initial_state)

print("The first set of available actions {0}".format(available_act))

# This function chooses at random which action to be performed within the range
# of all the available actions.
def sample_next_action(available_actions_range):
    next_action = int(np.random.choice(available_act, 1))
    return next_action


# Sample next action to be performed
action = sample_next_action(available_act)


# This function updates the Q matrix according to the path selected and the Q
# learning algorithm
def update(current_state, action, gamma):
    max_index = np.where(Q[action,] == np.max(Q[action,]))[1]

    if max_index.shape[0] > 1:
        max_index = int(np.random.choice(max_index, size=1))
    else:
        max_index = int(max_index)
    max_value = Q[action, max_index]

    Q[current_state, action] = R[current_state, action] + gamma * max_value
    print('max_value', R[current_state, action] + gamma * max_value)

    if (np.max(Q) > 0):
        return (np.sum(Q / np.max(Q) * 100))
    else:
        return (0)

# Update Q matrix
update(initial_state, action, gamma)

# -------------------------------------------------------------------------------
# Training


# Train over 10 000 iterations. (Re-iterate the process above).
scores = []
for i in range(1000):
    # Pattern:
    #   Find current state -> availabel act -> pick action -> update q value
    current_state = np.random.randint(0, int(Q.shape[0]))
    available_act = available_actions(current_state)
    if len(available_act) > 0:
        action = sample_next_action(available_act)
        score = update(current_state, action, gamma)
        scores.append(score)
    print(i % 50)
    if i % 50 == 0:
        print("Q for each 50 iterations")
        print(Q/ np.max(Q) * 100)

# Normalize the "trained" Q matrix
print("Trained Q matrix:")
print(Q / np.max(Q) * 100)

# -------------------------------------------------------------------------------
# Testing

# Goal state = 5
# Best sequence path starting from 2 -> 2, 3, 1, 5



np.set_printoptions(formatter={'float': '{: 0.1f}'.format})

print("The R (rewards) matrix which should stay constant {0}".format(R))
print("The Q matrix is {0}".format(Q))
print("The Q matrix type is {0}".format(type(Q)))
print("The scores are {0}".format(scores))
plt.plot(scores)
plt.show()

print("Calculating the shortest path")
current_state = 0
steps = [current_state]

while current_state != 15:

    next_step_index = np.where(Q[current_state,] == np.max(Q[current_state,]))[1]

    if next_step_index.shape[0] > 1:
        next_step_index = int(np.random.choice(next_step_index, size=1))
    else:
        next_step_index = int(next_step_index)

    steps.append(next_step_index)
    current_state = next_step_index
    print("In while loop")
# Print selected sequence of steps
print("Selected path:")
print(steps)

