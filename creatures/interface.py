from abc import ABC, abstractmethod

class MovingCreature(ABC):
    
    @abstractmethod
    def __init__(self, x: int, y: int):
        pass
    
    @abstractmethod
    def move(self):
        pass