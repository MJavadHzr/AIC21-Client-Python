from Model import *
import random
from typing import *

# simple example which keep its last direction till face a wall,
# then report wall in chat box and randomly continues its way
# also report in case of resource detection


class AI:
    last_dir: int = Direction.UP.value

    def __init__(self):
        # Current Game State
        self.game: Game = None

        # Answer
        self.message: str = None
        self.direction: int = None
        self.value: int = None

    def get_xy_value_of_direction(self, dir):
        switcher = {
            Direction.CENTER.value: (0, 0),
            Direction.RIGHT.value: (1, 0),
            Direction.UP.value: (0, -1),
            Direction.LEFT.value: (-1, 0),
            Direction.DOWN.value: (0, 1),
        }
        return switcher.get(dir, -1)

    def is_wall_cell(self, agent: Ant, relative_pos):
        neighbor_cell = agent.getMapRelativeCell(
            x=relative_pos[0],
            y=relative_pos[1]
        )
        return neighbor_cell.type == CellType.WALL.value

    def is_resource_cell(self, agent: Ant, relative_pos):
        neighbor_cell = agent.getMapRelativeCell(
            x=relative_pos[0],
            y=relative_pos[1]
        )
        return (neighbor_cell.resource_type == ResourceType.BREAD.value) or (neighbor_cell.resource_type == ResourceType.GRASS.value)

    def turn(self):
        agent = self.game.ant
        game = self.game

        # first check chat box
        for chat in game.chatBox.allChats:
            print('message: {}, turn:{}'.format(chat.text, chat.turn))

        # assume next step is empty cell
        relative_pos = self.get_xy_value_of_direction(AI.last_dir)
        self.message = 'empty @ [{}, {}]'.format(
            agent.currentX + relative_pos[0],
            agent.currentY + relative_pos[1]
        )
        self.direction = AI.last_dir
        self.value = 1

        # check if there is a wall
        if self.is_wall_cell(agent, relative_pos):
            # report we have found a wall
            self.message = 'wall @ [{}, {}]'.format(
                agent.currentX + relative_pos[0],
                agent.currentY + relative_pos[1]
            )

            # choose a random direction
            directions = [Direction.UP, Direction.RIGHT,
                          Direction.DOWN, Direction.LEFT]

            while self.is_wall_cell(agent, relative_pos):
                random.shuffle(directions)
                self.direction = random.choice(directions).value
                relative_pos = self.get_xy_value_of_direction(self.direction)

            AI.last_dir = self.direction
            self.value = 3

        # check if there is resource
        elif self.is_resource_cell(agent, relative_pos):
            # report we have found a resource
            neighbore_cell = agent.getMapRelativeCell(
                x=relative_pos[0],
                y=relative_pos[1]
            )

            self.message = 'resource @ [{}, {}], type:{}, value:{}'.format(
                neighbore_cell.x,
                neighbore_cell.y,
                neighbore_cell.resource_type,
                neighbore_cell.resource_value
            )

            self.value = 5

        # return answer
        return(self.message, self.value, self.direction)
