import random
import itertools

from labyrinth.cell import *
from objects.implementation import Treasure


class Labyrinth:
    
    def __init__(self, size):
        self.size = size
        self.size_sq = size ** 2
        self.cells = [[Cell(x, y, set(['up', 'down', 'right', 'left'])) for y in range(self.size)] 
                      for x in range(self.size)]
        
        self.symbols = {(): '┼', ('left'): '├', ('down'): '┴', ('up'): '┬',
                        ('up', 'left'): '┌', ('down', 'left'): '└', ('up', 'down'): '─',
                        ('up', 'down', 'left'): '╶', ('right'): '┤', ('right', 'left'): '│',
                        ('down', 'right'): '┘', ('up', 'right'): '┐', ('up', 'right', 'left'): '╷', 
                        ('down', 'right', 'left'): '╵', ('up', 'down', 'right'): '╴'}
      
    
    def neighbors(self, cell):
        x = cell.x
        y = cell.y
        res = []
        
        for new_x, new_y in [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)]:
            if 0 <= new_x < self.size and 0 <= new_y < self.size:
                neighbor = self.cells[new_x][new_y]
                res.append(neighbor)
        
        return res
    
    
    def get_random_cell(self):
        cell = random.choice(self.cells)
        cell = random.choice(cell)
        
        return cell
      
        
    def create_maze(self):
        cell_stack = []
        cell = self.get_random_cell()
        n_visited_cells = 1

        while n_visited_cells < self.size_sq:
            neighbors = [c for c in self.neighbors(cell) if c.isolated()]
            if len(neighbors):
                neighbor = random.choice(neighbors)
                cell.connect(neighbor)
                cell_stack.append(cell)
                cell = neighbor
                n_visited_cells += 1
            else:
                cell = cell_stack.pop()
         
        
    def create_objects(self):
        idxs = [i for i in itertools.product(range(self.size), repeat=2)]
        obj_pos = random.sample(idxs, 6)
        
        self.treasure = obj_pos[0]
        self.treasure_item = Treasure()
        self.wormholes = obj_pos[1:]
        
        
    def goto_next_wormhole(self, x, y):
        idx = (self.wormholes.index((x, y)) + 1) % 5
        
        return self.wormholes[idx]
        
        
    def create_monolith(self):
        monolith_idxs = range(-1, self.size+1)
        self.monolith = []
        
        self.monolith += [(-1, i) for i in monolith_idxs]
        self.monolith += [(i, -1) for i in monolith_idxs]
        self.monolith += [(self.size, i) for i in monolith_idxs]
        self.monolith += [(i, self.size) for i in monolith_idxs]
        
        self.monolith = list(set(self.monolith))
        edges = [(-1, -1), (-1, self.size), (self.size, self.size), (self.size, -1)]
        self.exit = random.choice([i for i in self.monolith if i not in edges])
        
    
    def create_map(self):
        self.map = [[0 for i in range(self.size + 2)] 
                    for j in range(self.size + 2)]
        
        keys = list(self.symbols.keys())

        for i in range(self.size + 2):
            for j in range(self.size + 2):
                if (i-1, j-1) in self.monolith:
                    if (i-1, j-1) == self.exit:
                        self.map[i][j] = ' '
                    else:
                        self.map[i][j] = '#'
                else:
                    if (i-1, j-1) in self.wormholes:
                        self.map[i][j] = '@'
                    elif (i-1, j-1) == self.treasure:
                        self.map[i][j] = '$'
                    else:
                        for k in range(len(self.symbols)):
                            if set(self.cells[i-1][j-1].walls) == set(keys[k]):
                                self.map[i][j] = self.symbols[keys[k]]

                            elif len(self.cells[i-1][j-1].walls) == 0:
                                self.map[i][j] = self.symbols[()]

                            elif list(self.cells[i-1][j-1].walls)[0] == keys[k]:
                                self.map[i][j] = self.symbols[keys[k]]
            
            
    def create_labyrinth(self):
        self.create_maze()
        self.create_objects()
        self.create_monolith()
        self.create_map()
        
        return self


class LabyrinthFabric:
    
    def produce(self, size):
        self.labyrinth = Labyrinth(size)
        lab = self.labyrinth.create_labyrinth()
        
        return lab