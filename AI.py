from Model import *
import random

"""
simple example which keeps its last direction till face a wall,
then reports wall in chat box and randomly chooses a direction to move on
also reports resources in case of resource detection
"""


class AI:
    # static field to use in different turns
    last_dir: int = Direction.UP.value

    def __init__(self):
        # Current Game State
        self.game: Game = None

        # Answer
        self.message: str = None
        self.direction: int = None
        self.value: int = None

    # return (x, y) value of a direction
    def get_xy_value_of_direction(self, dir):
        switcher = {
            Direction.CENTER.value: (0, 0),
            Direction.RIGHT.value: (1, 0),
            Direction.UP.value: (0, -1),
            Direction.LEFT.value: (-1, 0),
            Direction.DOWN.value: (0, 1),
        }
        return switcher.get(dir, -1)

    # return TRUE if cell is wall
    def is_wall_cell(self, agent: Ant, relative_pos):
        neighbor_cell = agent.getMapRelativeCell(
            x=relative_pos[0],
            y=relative_pos[1]
        )
        return neighbor_cell.type == CellType.WALL.value

    # return TRUE if cell has any resource
    def is_resource_cell(self, agent: Ant, relative_pos):
        neighbor_cell = agent.getMapRelativeCell(
            x=relative_pos[0],
            y=relative_pos[1]
        )
        return (neighbor_cell.resource_type == ResourceType.BREAD.value) or (neighbor_cell.resource_type == ResourceType.GRASS.value)

    # main function of AI
    def turn(self):
        agent = self.game.ant
        game = self.game

        # first check chat box
        for chat in game.chatBox.allChats:
            print('message: {}, turn:{}'.format(chat.text, chat.turn))

        # get relative position of next cell base on chosen direction
        relative_pos = self.get_xy_value_of_direction(AI.last_dir)

        # assume next step is empty cell
        self.message = 'empty @ [{}, {}]'.format(
            agent.currentX + relative_pos[0],
            agent.currentY + relative_pos[1]
        )
        self.direction = AI.last_dir
        self.value = 1

        # check if there is a wall
        if self.is_wall_cell(agent, relative_pos):
            # set message of finding wall
            self.message = 'wall @ [{}, {}]'.format(
                agent.currentX + relative_pos[0],
                agent.currentY + relative_pos[1]
            )

            # list of all possible directions we can choose except [center]
            directions = [Direction.UP, Direction.RIGHT,
                          Direction.DOWN, Direction.LEFT]

            # keep choosing randomly while next cell is wall
            while self.is_wall_cell(agent, relative_pos):
                self.direction = random.choice(directions).value
                relative_pos = self.get_xy_value_of_direction(self.direction)

            # save last_dir to use in next turn
            AI.last_dir = self.direction
            self.value = 3

        # check if there is resource
        elif self.is_resource_cell(agent, relative_pos):
            # get next cell from agent
            neighbore_cell = agent.getMapRelativeCell(
                x=relative_pos[0],
                y=relative_pos[1]
            )

            # set message of finding resource
            self.message = 'resource @ [{}, {}], type:{}, value:{}'.format(
                neighbore_cell.x,
                neighbore_cell.y,
                neighbore_cell.resource_type,
                neighbore_cell.resource_value
            )

            # set message value
            self.value = 5

        # return answer
        return(self.message, self.value, self.direction)
