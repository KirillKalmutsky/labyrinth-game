class Cell:
    
    def __init__(self, x, y, walls):
        
        self.x = x
        self.y = y
        self.walls = walls

        self.seen = False
      
    
    def direction(self, cell_to):
        if abs(self.x - cell_to.x) + abs(self.y - cell_to.y) == 1:
            if cell_to.y < self.y:
                return 'up'
            elif cell_to.y > self.y:
                return 'down'
            elif cell_to.x < self.x:
                return 'left'
            elif cell_to.x > self.x:
                return 'right'
            else:
                return False
        else:
            return False
        
        
    def connect(self, cell_to):
        cell_to.walls.remove(cell_to.direction(self))
        self.walls.remove(self.direction(cell_to))
        
        
    def isolated(self):
        return len(self.walls) == 4
    
    
    def explored(self):
        self.seen = True