# Grid_World Version 1
# This program allows a player to play a memory game.
# The player selects tiles on a 4x4 board. When a tile is
# selected, an image is exposed until a second image is
# selected. If the two images match, the tiles remain
# exposed and one point is added to the score.
# If the exposed image does not match, both tiles remain
# exposed for one second, then they are hidden.
# Selecting an exposed image has no effect.
# The game ends when all tiles are exposed.
# The score is the time taken to expose all tiles so a lower
# score is better.
# This program requires 9 data files: image0 ... image8,
# where image0 is the hidden form of all tiles and image1
# ... image8 are the exposed tile images.
import numpy as np
from helpers_qlearning import *
import matplotlib.pyplot as plt
import math
import pygame, sys, time, random
from pygame.locals import *
import numpy as np
action_dict = {'0': "Up",
               '1': "Down",
               '2': "Right",
               '3': "Left",
               }
# User-defined classes

supress_print = True

class Tile:
    # An object in this class represents a single Tile that
    # has an image

    # initialize the class attributes that are common to all
    # tiles.

    borderColor = pygame.Color('black')
    borderWidth = 4  # the pixel width of the tile border
    image = pygame.image.load('RL_mike.png')
    image = pygame.transform.scale(image, (100, 100))

    def __init__(self, x, y, wall, surface, tile_size = (100,100)):
        # Initialize a tile to contain an image
        # - x is the int x coord of the upper left corner
        # - y is the int y coord of the upper left corner
        # - image is the pygame.Surface to display as the
        # exposed image
        # - surface is the window's pygame.Surface object

        self.wall = wall
        self.origin = (x, y)
        self.tile_coord = [x//100, y//100]
        self.surface = surface
        self.tile_size = tile_size

    def draw(self, pos, goal):
        # Draw the tile.

        rectangle = pygame.Rect(self.origin, self.tile_size)
        if self.wall:
            pygame.draw.rect(self.surface, pygame.Color('gray'), rectangle, 0)
        elif goal == self.tile_coord:
            pygame.draw.rect(self.surface, pygame.Color('green'), rectangle, 0)
        else:
            pygame.draw.rect(self.surface, pygame.Color('white'), rectangle, 0)

        if pos == self.tile_coord:
            self.surface.blit(Tile.image, self.origin)




        pygame.draw.rect(self.surface, Tile.borderColor, rectangle, Tile.borderWidth)


class Grid_World():
    # An object in this class represents a Grid_World game.
    tile_width = 100
    tile_height = 100
    def __init__(self, surface, board_size = (6,9), wall_coords=[], start_coord=(0,0), goal_coord=(5,8)):
        # Intialize a Grid_World game.
        # - surface is the pygame.Surface of the window

        self.surface = surface
        self.bgColor = pygame.Color('black')
        self.board_size = list(board_size)
        if not wall_coords:
            #self.wall_coords = [[2,i] for i in range(board_size[1]-1)]
            self.wall_coords = [[1,0,], [1,1], [1,3]]
        else:
            self.wall_coords = wall_coords


        self.start_coord = list(start_coord)
        self.goal_coord = list(goal_coord)
        self.position = list(start_coord)
        self.actions = range(4)
        self.reward = 0

        self.calc_wall_coords()
        self.createTiles()

    def calc_wall_coords(self):
        self.board_wall_coords = [[self.board_size[0] - x - 1, y] for x, y in self.wall_coords]

    def find_board_coords(self, pos):
        x = pos[1]
        y = self.board_size[0] - pos[0] -1
        return [x,y]

    def createTiles(self):
        # Create the Tiles
        # - self is the Grid_World game
        self.board = []
        for rowIndex in range(0, self.board_size[0]):
            row = []
            for columnIndex in range(0, self.board_size[1]):
                imageIndex = rowIndex * self.board_size[1] + columnIndex
                x = columnIndex * Grid_World.tile_width
                y = rowIndex * Grid_World.tile_height
                if [rowIndex,columnIndex] in self.board_wall_coords:
                    wall = True
                else:
                    wall = False
                tile = Tile(x, y, wall, self.surface)
                row.append(tile)
            self.board.append(row)

    def draw(self):
        # Draw the tiles.
        # - self is the Grid_World game
        pos = self.find_board_coords(self.position)
        goal = self.find_board_coords(self.goal_coord)
        self.surface.fill(self.bgColor)
        for row in self.board:
            for tile in row:
                tile.draw(pos, goal)

    def update(self):
        # Check if the game is over. If so return True.
        # If the game is not over,  draw the board
        # and return False.
        # - self is the TTT game

        if self.position == self.goal_coord:
            return True
        else:
            self.draw()
            return False

    def step(self, action):
        x,y = self.position
        if action == 0:   # Action Up
            # print "Up"
            # Check for wall coordinates and for boarder
            if [x+1,y] not in self.wall_coords and x+1 < self.board_size[0]:
                self.position = [x+1,y]

        elif action == 1:   # Action Down
            # print "Down"
            # Check for wall coordinates and for boarder
            if [x-1,y] not in self.wall_coords and x-1 >= 0:
                self.position = [x-1,y]

        elif action == 2:   # Action Right
            # print "Right"
            # Check for wall coordinates and for boarder
            if [x,y+1] not in self.wall_coords and y+1 < self.board_size[1]:
                self.position = [x,y+1]

        elif action == 3:   # Action Left
            # print "Left"
            # Check for wall coordinates and for boarder
            if [x,y-1] not in self.wall_coords and y-1 >= 0 :
                self.position = [x,y-1]

        # Reward definition
        if self.position == self.goal_coord:
            self.reward = 1
        else:
            self.reward = 0
        #print action_dict[str(action)], self.position

    def change_the_wall(self, wall_coords):
        self.wall_coords = wall_coords
        self.calc_wall_coords()
        self.createTiles()

    def change_the_goal(self, goal):
        self.goal_coord = list(goal)



if __name__ == "__main__":
    ####

    # Set up the grid world #

    ####
    # Initialize pygame
    pygame.init()

    # Set window size and title, and frame delay

    surfaceSize = (1000, 600)
    windowTitle = 'Grid_World'
    pauseTime = 1  # smaller is faster game

    # Refactor the grid world size
    grid_dimension = (4.0, 4.0)
    grid_dimension_int = (int(grid_dimension[0]),int(grid_dimension[1]))
    surface_height = grid_dimension[0] / 6.0 * 1000
    surface_width = 6 / 9.0 * 600
    goal_cell = (grid_dimension[0]-1, grid_dimension[1]-1)

    # Create the integer surface size

    surfaceSize = (int(math.ceil(surface_height)), int(math.ceil(surface_width)))

    # Create the window
    surface = pygame.display.set_mode(surfaceSize, 0, 0)
    pygame.display.set_caption(windowTitle)

    # create and initialize objects
    gameOver = False

    # Set goal to be dependent on the height and width of the grid.

    R = np.matrix([[-1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                   [0, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                   [-1, 0, -1, -0, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                   [-1, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                   [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                   [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                   [-1, -1, 0, -1, -1, -1, -1, -1, -1, -1, 0, -1, -1, -1, -1, -1],
                   [-1, -1, -1, 0, -1, -1, 0, -1, -1, -1, -1, 0, -1, -1, -1, -1],
                   [-1, -1, -1, -1, -1, -1, -1, -1, -1, 0, -1, -1, 0, -1, -1, -1],
                   [-1, -1, -1, -1, -1, -1, -1, -1, 0, -1, 0, -1, -1, 0, -1, -1],
                   [-1, -1, -1, -1, -1, -1, 0, -1, -1, 0, -1, 0, -1, -1, 0, -1],
                   [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, -1, -1, -1, -1, 100],
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
            print("The current state {0}".format(np.where(current_state_row >= 0)[0]))
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
    counter = 0
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
        if i % 10 == 0:
            counter += 1
            print("Sample for the {0} sim ".format(i))

            board = Grid_World(surface,grid_dimension_int, goal_coord=goal_cell)

            # Draw objects
            board.draw()

            # Refresh the display
            pygame.display.update()

            my_action = 2



            # Loop forever
            while True:
                # Handle events
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                        # Handle additional events

                # Update and draw objects for next frame
                gameOver = board.update()
                print("The current position: {0}".format(board.position))

                prev_position = board.position


                # My code
                one_dimension_board = board.position[0] * grid_dimension_int[1] + board.position[1]
                new_action = my_action
                print("The one dimension board is: {0}".format(one_dimension_board))
                av_actions = Q[one_dimension_board,]
                transition_state = np.argmax(Q[one_dimension_board,])
                print("The possible actions {0}".format(Q[one_dimension_board,]))
                print("The transition state {0}".format(transition_state))
                print("THe max value of Q[state,]: {0}".format(np.max(Q[one_dimension_board,])))
                if((transition_state - one_dimension_board) > 1):
                    new_action = 0
                if ((transition_state - one_dimension_board) < 1):
                    new_action = 1
                if ((transition_state - one_dimension_board) == 1):
                    new_action = 2
                if ((transition_state - one_dimension_board) == -1):
                    new_action = 3
                if ((transition_state - one_dimension_board) == 0) or np.max(Q[one_dimension_board,]) <= 0.0:
                    new_action = np.random.choice(4,1)[0]



                print("The action is {0}".format(new_action))
                #if prev_position == board.position:
                #    while new_action == my_action:
                #        new_action = np.random.choice(4,1)[0]
                #        print("The new action {0}".format(new_action))




                if gameOver:
                    break

                # Refresh the display
                board.step(new_action)
                pygame.display.update()

                my_action = new_action

                # Set the frame speed by pausing between frames
                time.sleep(0.5)

