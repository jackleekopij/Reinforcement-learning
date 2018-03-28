import numpy as np





def create_reward_matrix(grid_coords, wall_coords, goal_coords, reward):
    """
    create_reward_matrx will create a transition reward matrix.
    :param grid_coords: the coordinates of the grid world
    :param wall_coords: the coordinates of the walls in the world
    :param goal_coords:
    :return:
    """
    height = grid_coords[0]
    width = grid_coords[1]
    transition_states = height * width
    initialised_transition_matrix = np.zeros((transition_states,transition_states)) - 1
    print("Number of rows: {0}".format(len(initialised_transition_matrix)))
    print("Number of columns: {0}".format(len(initialised_transition_matrix[0])))



    # Set the bottom boundary transition upwards
    for i in range(width):
        initialised_transition_matrix[i,i+width] = 0

    # Set top conditions
    for i in range(width):
        initialised_transition_matrix[i + (height-1) * width, i + (height-2) * width] = 0

    # Set the left border transition right
    for i in range(height):
        initialised_transition_matrix[i * width, i * width + 1] = 0

    # Set the right border transition left
    for i in range(1, height + 1):
        initialised_transition_matrix[i * width - 1, i * width - 2] = 0

    if height > 2:
        for j in range(1,height-1):
            for i in range(width):
                print("Height {0}".format(j))
                initialised_transition_matrix[i + (j) * width, i + (j - 1) * width] = 0
                initialised_transition_matrix[i + (j) * width, i + (j + 1) * width] = 0

    # This will create a between a node and its neighbours both left and right.
    # Note: if width <= 2 no squares can have both a left and right neighbour
    if width > 2:
        for j in range(1,width-1):
            # Set the left border transition right
            for i in range(height):
                initialised_transition_matrix[j + i * width, j + i * width + 1] = 0
                initialised_transition_matrix[j + i * width, j + i * width - 1] = 0

    # What boundary conditions do we have... borders, walls and goals


    if len(wall_coords) > 0:
        print("IN walll coords")
        for wall in wall_coords:
            # Get one-dimensional coordinate...
            # Should be integer
            one_dim_coord = wall[0] * width + wall[1]
            # Minus one because Python starts counting at zero but our scale starts at zero.
            initialised_transition_matrix[one_dim_coord,] = -1
            initialised_transition_matrix[:,one_dim_coord] = -1



    # Set transition reward from left and right of the goal
    if len(goal_coords) > 0:
        # Set goal to goal to be absorbing
        absorbing_index = (goal_coords[0] + 1) * (goal_coords[1] + 1) - 1
        print("The index of the absorbing state {0}".format(absorbing_index))
        initialised_transition_matrix[absorbing_index, absorbing_index] = reward

        # get square left
        if goal_coords[1] == width - 1:
            one_dim_coord = goal_coords[0] * width + goal_coords[1]
            initialised_transition_matrix[one_dim_coord - 1, one_dim_coord] = reward
        elif goal_coords[1] == 0:
            one_dim_coord = goal_coords[0] * width + goal_coords[1]
            initialised_transition_matrix[one_dim_coord + 1, one_dim_coord] = reward
        else:
            one_dim_coord = goal_coords[0] * width + goal_coords[1]
            initialised_transition_matrix[one_dim_coord - 1, one_dim_coord] = reward
            initialised_transition_matrix[one_dim_coord + 1, one_dim_coord] = reward

        if goal_coords[0] == height - 1:
            one_dim_coord = goal_coords[0]  * width + goal_coords[1]
            initialised_transition_matrix[one_dim_coord - width, one_dim_coord] = reward
        elif goal_coords[0] == 0:
            one_dim_coord = goal_coords[0]  * width + goal_coords[1]
            initialised_transition_matrix[one_dim_coord + width, one_dim_coord] = reward
        else:
            one_dim_coord = goal_coords[0] * width + goal_coords[1]
            initialised_transition_matrix[one_dim_coord + width, one_dim_coord] = reward
            initialised_transition_matrix[one_dim_coord - width, one_dim_coord] = reward

    print(initialised_transition_matrix)
    return initialised_transition_matrix


