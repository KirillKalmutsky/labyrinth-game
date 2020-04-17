import random
import itertools
import pickle
import os

from labyrinth.labyrinth import *
from creatures.implementation import *
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
                         'go': self.move
                        }
        
        self.move_commands = {'go up': ('up', 0, -1), 
                              'go down': ('down', 0, 1),
                              'go left': ('left', -1, 0),
                              'go right': ('right', 1, 0),
                             }
    
    
    def quit(self, command):
        print('The game is closed')
        
        return False
    
    
    def skip(self, command):
        if (self.player.x, self.player.y) in self.labyrinth.wormholes:
            print('You falled into wormhole!')
            self.player.x, self.player.y = self.labyrinth.goto_next_wormhole(self.player.x, self.player.y)
            self.labyrinth.cells[self.player.x][self.player.y].explored()
        else:
            print('You skipped your turn')
        
        return True
    
    
    def pos(self, command):
        print(self.player.x, self.player.y)
        
        return True
    
    
    def clear(self, command):
        os.system('clear')
        
        return True
     
    
    def exit(self, command):
        print(self.labyrinth.exit)
        
        return True
    
    
    def inventory(self, command):
        if self.player.inventory:
            for item in self.player.inventory:
                print(item)
        else:
            print('Your inventory is empty')
        
        return True
    
    
    def save(self, command):
        filename = command.split()[1]
        
        with open(os.path.join('saves', filename) + '.pkl', 'wb') as output:
            pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)
        
        print(f'Game has been saved as {filename}')
        
        return False
    
    
    def move(self, command):
        direction, difx, dify = self.move_commands[command]
        
        if (self.player.x + difx, self.player.y + dify) in self.labyrinth.monolith:
            if (self.player.x + difx, self.player.y + dify) == self.labyrinth.exit:
                if self.player.check_item(self.labyrinth.treasure_item):
                    print('You found the treasure and left the labyrinth!')
                    self.__won = True
                    return True
                else:
                    self.player.exit_seen = True
                    print("You cannot leave the labyrinth until you find the treasure")
                    return True
            else:
                print("step impossible, monolith")
                return True
            
        elif direction in self.labyrinth.cells[self.player.x][self.player.y].walls:
            print("step impossible, wall")
            return True
            
        else:
            self.player.move(direction)
            self.labyrinth.cells[self.player.x][self.player.y].explored()
                
            if (self.player.x, self.player.y) == self.labyrinth.treasure:
                self.player.get_item(self.labyrinth.treasure_item)
                self.labyrinth.treasure = None
                print("step executed, treasure")
                return True
                
            elif (self.player.x, self.player.y) in self.labyrinth.wormholes:
                print("step executed, wormhole")
                return True
                
            else:
                print("step executed")
                return True
            

    def print_labyrinth(self, command):
        self.clear(command)
        for i in range(len(self.labyrinth.map)):
            for j in range(len(self.labyrinth.map)):
                print(self.labyrinth.map[j][i], end='')
            print()
        return True
    
    
    def print_seen_part(self, command):
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
        return True
            
    
    def show_me(self, command):
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
                        print(self.labyrinth.map[j][i], end='')
                    else:
                        print('#', end='')    
                except IndexError:
                    print(self.labyrinth.map[j][i], end='')
            
            print()
        return True
      
    
    def play(self, loaded=False):
           
        if not loaded:
            initial_cell = self.labyrinth.get_random_cell()
            self.player = Player(initial_cell.x, initial_cell.y)
            self.labyrinth.cells[self.player.x][self.player.y].explored()
            self.__won = False
        
        while not self.__won:
            try:
                command = input()
                result = self.commands[command.split()[0]](command)

                if not result:
                    return False
            
            except KeyError:
                print('Unknown command')
                
        print('You won!')
        return True