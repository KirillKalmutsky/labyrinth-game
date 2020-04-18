from abc import ABC, abstractmethod


class Menu(ABC):
    
    @abstractmethod
    def new_game(self):
        pass
    
    
    @abstractmethod
    def load_game(self):
        pass