import random
import itertools
import pickle
import os

from game.labyrinth_game import LabyrinthGame
from game.utils import parse_command, load_game
from labyrinth.labyrinth import LabyrinthFabric


if __name__ == '__main__':
    command = parse_command()
    if command:
        if command[0]:
            fabric = LabyrinthFabric()
            new_game = LabyrinthGame(fabric.produce(command[1]))
            print('New game has started')
            new_game.play(loaded=False)
        
        else:
            loaded_game = load_game(command[1])
            print('Loaded game has started')
            loaded_game.play(loaded=True)