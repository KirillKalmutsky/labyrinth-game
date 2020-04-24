import pickle
import os

from menu.interface import Menu
from labyrinth.labyrinth import LabyrinthFabric
from game.labyrinth_game import LabyrinthGame


class LabyrinthMenu(Menu):
    
    
    def start(self):
        print('Type command "start <labyrinth_size>", "load <file_name>" or "quit"')
        
        while True:
            
            self.command = input().split()
            if not self.command:
                continue
                
            if self.command[0] == 'start':
                self.command[1] = int(self.command[1])
                if (self.command[1] < 4) or (self.command[1] > 10):
                    print('Size must be not less 4 and not bigger 10')
                    continue
                return self.new_game()
            
            elif self.command[0] == 'debug':
                self.command[1] = int(self.command[1])
                if (self.command[1] < 4) or (self.command[1] > 10):
                    print('Size must be not less 4 and not bigger 10')
                    continue
                return self.new_game(debug_mode=True)
            
            elif self.command[0] == 'load':
                self.command[1] = self.command[1] + '.pkl'
                return self.load_game()
            
            elif self.command[0] == 'quit':
                return False
            
            else:
                print('Unknown command, try again or type "quit"')
    
    
    def new_game(self, debug_mode=False):
        fabric = LabyrinthFabric()
        new_game = LabyrinthGame(fabric.produce(self.command[1]))
        print('New game has started')
        
        return new_game.play(debug_mode=debug_mode)
    
    
    def load_game(self):
        with open(os.path.join('saves', self.command[1]), 'rb') as f:
            loaded_game = pickle.load(f)
            
        print('Loaded game has started')
        
        return loaded_game.play(loaded=True)