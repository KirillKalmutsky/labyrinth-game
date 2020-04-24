import random
import itertools
import pickle
import os

from labyrinth.labyrinth import *
from creatures.player import Player
from creatures.bear import Bear
from objects.implementation import Treasure


class LabyrinthGame:
    
    def __init__(self, labyrinth):
        self.labyrinth = labyrinth
        
        self.commands = {'quit': self.quit,
                         'skip': self.skip,
                         'pos': self.pos,
                         'clear': self.clear,
                         'inventory': self.inventory,
                         'exit': self.exit,
                         'map': self.print_seen_part,
                         'full_map': self.print_labyrinth,
                         'save': self.save,
                         'me': self.show_me,
                         'help': self.allcommands,
                         'go': self.move,
                         'hp': self.get_hp,
                        }
        
        self.move_commands = {'go up': ('up', 0, -1), 
                              'go down': ('down', 0, 1),
                              'go left': ('left', -1, 0),
                              'go right': ('right', 1, 0),
                             }
    
    
    def allcommands(self, command):
        '''Print all commands'''
        self.clear(command)
        
        for name, func in self.commands.items():
            print(f"'{name}': {func.__doc__}")
            
        return True
    
    
    def quit(self, command):
        '''Quit the game'''
        print('The game is closed')
        
        return False
    
    
    def skip(self, command):
        '''Skip your turn, fall into warmhole'''
        if (self.player.x, self.player.y) in self.labyrinth.river:
            idx = self.labyrinth.river.index((self.player.x, self.player.y))
            if idx + 2 < len(self.labyrinth.river):
                self.player.x, self.player.y = self.labyrinth.river[idx + 2]
                print('Skip move on the river, moved 2 steps down the river')
            else:
                self.player.x, self.player.y = self.labyrinth.river[-1]
                print('Skip move on the river, moved to estuary!')
                
        elif (self.player.x, self.player.y) in self.labyrinth.wormholes:
            print('You falled into wormhole!')
            self.player.x, self.player.y = self.labyrinth.goto_next_wormhole(self.player.x, self.player.y)
            self.labyrinth.cells[self.player.x][self.player.y].explored()
        else:
            print('You skipped your turn')
        
        return True
    
    
    def pos(self, command):
        '''Get your current position'''
        print(self.player.x, self.player.y)
        
        return None
    
    
    def clear(self, command):
        '''Clear output in console'''
        os.system('clear')
        
        return None
     
    
    def exit(self, command):
        '''Position of exit, cheating'''
        print(self.labyrinth.exit)
        
        return None
    
    
    def inventory(self, command):
        '''Open your inventory'''
        if self.player.inventory:
            for item in self.player.inventory:
                print(item)
        else:
            print('Your inventory is empty')
        
        return None
    
    
    def save(self, command):
        '''Save and quit the game'''
        filename = command.split()[1]
        
        with open(os.path.join('saves', filename) + '.pkl', 'wb') as output:
            pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)
        
        print(f'Game has been saved as {filename}')
        
        return False
    
    
    def move(self, command):
        '''Move into one direction of: "up", "down", "right", "left"'''
        direction, difx, dify = self.move_commands[command]
        
        if (self.player.x + difx, self.player.y + dify) in self.labyrinth.river:
            if (self.player.x, self.player.y) not in self.labyrinth.river:
                idx = self.labyrinth.river.index((self.player.x + difx, self.player.y + dify))
                if idx + 2 < len(self.labyrinth.river):
                    self.player.x, self.player.y = self.labyrinth.river[idx + 2]
                    print('You reach the river, moved 2 steps down the river!')
                    return True
                
                else:
                    self.player.x, self.player.y = self.labyrinth.river[-1]
                    print('You reach the river, moved to estuary!')
                    return True
            
        
        if (self.player.x + difx, self.player.y + dify) in self.labyrinth.monolith:
            if (self.player.x + difx, self.player.y + dify) == self.labyrinth.exit:
                if self.player.check_item(self.labyrinth.treasure_item):
                    print('You found the treasure and left the labyrinth!')
                    self.__won = True
                else:
                    self.player.exit_seen = True
                    print("You cannot leave the labyrinth until you find the treasure")
            else:
                print("step impossible, monolith")
                return None
            
        elif direction in self.labyrinth.cells[self.player.x][self.player.y].walls:
            print("step impossible, wall")
            return None
            
        else:
            self.player.move(direction)
            self.labyrinth.cells[self.player.x][self.player.y].explored()
                
            if (self.player.x, self.player.y) == self.labyrinth.treasure:
                self.player.get_item(self.labyrinth.treasure_item)
                self.labyrinth.treasure = None
                print("step executed, treasure")
                
            elif (self.player.x, self.player.y) in self.labyrinth.wormholes:
                print("step executed, wormhole")
            elif (self.player.x, self.player.y) in self.labyrinth.river:
                print("step executed, river")   
            else:
                print("step executed")
        
        return True
            

    def print_labyrinth(self, command):
        '''Print all labyrinth, cheating'''
        self.clear(command)
        for i in range(len(self.labyrinth.map)):
            for j in range(len(self.labyrinth.map)):
                if (i-1, j-1) == (self.player.y, self.player.x):
                    print('x', end='')
                elif (i-1, j-1) == (self.bear.y, self.bear.x):
                    print('B', end='')
                else:
                    print(self.labyrinth.map[j][i], end='')
            print()
        return None
    
    
    def print_seen_part(self, command):
        '''Print seen part of labyrinth'''
        self.clear(command)
        for i in range(len(self.labyrinth.map)):
            for j in range(len(self.labyrinth.map)):
                if self.labyrinth.map[j][i] == ' ' and not self.player.exit_seen:
                    print('#', end='')
                    continue
                try:
                    if self.labyrinth.cells[j-1][i-1].seen:
                        print(self.labyrinth.map[j][i], end='')
                    else:
                        print('#', end='')    
                except IndexError:
                    print(self.labyrinth.map[j][i], end='')
            
            print()
        return self.skip(command)
            
    
    def show_me(self, command):
        '''Print labyrinth with you as "x" mark and bear as "B" mark if his cell is seen'''
        self.clear(command)
        for i in range(len(self.labyrinth.map)):
            for j in range(len(self.labyrinth.map)):
                if self.labyrinth.map[j][i] == ' ' and not self.player.exit_seen:
                    print('#', end='')
                    continue
                if (i-1, j-1) == (self.player.y, self.player.x):
                    print('x', end='')
                    continue
                try:
                    if self.labyrinth.cells[j-1][i-1].seen:
                        if (i-1, j-1) == (self.bear.y, self.bear.x):
                            print('B', end='')
                        else:
                            print(self.labyrinth.map[j][i], end='')
                    else:
                        print('#', end='')    
                except IndexError:
                    print(self.labyrinth.map[j][i], end='')
            
            print()
        return self.skip(command)
    
    
    def bear_walking(self):
        '''Random walking without tracing'''
        
        walls = set(['up', 'down', 'right', 'left', 'skip'])
        directions = list(walls.difference(self.labyrinth.cells[self.bear.x][self.bear.y].walls))
        moves = []
        
        # To lower probability of skip
        for move in directions:
            if move == 'skip':
                moves.append(move)
            else:
                for _ in range(2):
                    moves.append(move)
        
        # Pick random action
        action = random.choice(moves)
        
        if action == 'skip':
            if (self.bear.x, self.bear.y) in self.labyrinth.river:
                idx = self.labyrinth.river.index((self.bear.x, self.bear.y))
                if idx + 2 < len(self.labyrinth.river):
                    self.bear.x, self.bear.y = self.labyrinth.river[idx + 2]
                else:
                    self.bear.x, self.bear.y = self.labyrinth.river[-1]
            
            elif (self.bear.x, self.bear.y) in self.labyrinth.wormholes:
                self.bear.x, self.bear.y = self.labyrinth.goto_next_wormhole(self.bear.x, self.bear.y)
        else:
            command = 'go ' + action
            direction, difx, dify = self.move_commands[command]
            
            if (self.bear.x + difx, self.bear.y + dify) in self.labyrinth.river:
                if (self.bear.x, self.bear.y) not in self.labyrinth.river:
                    idx = self.labyrinth.river.index((self.bear.x + difx, self.bear.y + dify))
                    
                    if idx + 2 < len(self.labyrinth.river):
                        self.bear.x, self.bear.y = self.labyrinth.river[idx + 2]
                    else:
                        self.bear.x, self.bear.y = self.labyrinth.river[-1]
            
            else:
                self.bear.move(direction)
            
            
        if (self.bear.x, self.bear.y) == (self.player.x, self.player.y):
            self.bear.hit(self.player)
            
            walls = set(['up', 'down', 'right', 'left'])
            directions = list(walls.difference(self.labyrinth.cells[self.bear.x][self.bear.y].walls))
            action = random.choice(directions)
            command = 'go ' + action

            print('You got bited by bear!')
            print(f'Your current hp is: {self.player.hp}')
            
            if self.player.hp <= 0:
                return False
            
            print()
            print(f'You pushed into direction: {action}')
            self.move(command)
        
        return True
    
    
    def get_hp(self, command):
        '''Get current hp of player'''
        print(f'Your current hp is: {self.player.hp}')
        
        return None
        
            
    def create_newgame(self):
        initial_cell_player = self.labyrinth.get_random_cell()
        initial_cell_bear = self.labyrinth.get_random_cell()
        
        while initial_cell_player == initial_cell_bear:
            initial_cell_bear = self.labyrinth.get_random_cell()
        
        self.player = Player(initial_cell_player.x, initial_cell_player.y)
        self.bear = Bear(initial_cell_bear.x, initial_cell_bear.y)
        
        self.labyrinth.cells[self.player.x][self.player.y].explored()
        self.__won = False
      
    
    def play(self, loaded=False, debug_mode=False):
           
        if not loaded:
            self.create_newgame()
        
        while not self.__won:
            try:
                if debug_mode:
                    self.clear(None)
                    self.print_labyrinth(None)
                    
                command = input()
                result = self.commands[command.split()[0]](command)
                
                # No step done, bear don't move
                if result is None:
                    continue
                
                # Quit the game
                if result is False:
                    return False
                
                result = self.bear_walking()
                
                # Killed by bear
                if result is False:
                    print('You died')
                    return False
            
            except (KeyError, IndexError):
                print('Unknown command')
                
        print('You won!')
        return True