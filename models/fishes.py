import random
from typing import List, Tuple, Optional
from abc import ABC, abstractmethod

class Fish(ABC):
    """Classe abstraite de base pour les espèces de poissons dans la simulation Wa-Tor."""
    def __init__(self, x=0, y=0, age=0):
        self.x = x
        self.y = y
        self.age = age
        self.reproduction_counter = 0
        self.moved = False
    
    def age_up(self):
        """Incrémente l'âge et le compteur de reproduction."""
        self.age += 1
        self.reproduction_counter += 1

    @abstractmethod
    def move(self, ocean):
        """Méthode abstraite qui doit être implémentée par les sous-classes."""
        pass

class Sardine(Fish):
    """Classe représentant une sardine, qui peut être mangée par les requins."""
    def __init__(self, x=0, y=0, age=0):
        super().__init__(x, y, age)
    
    def move(self, ocean):
        """Implémentation de la méthode abstraite de déplacement pour les sardines."""
        # Recherche des cases vides voisines
        empty_neighbors = []
        for nx, ny in ocean.get_neighbors(self.x, self.y):
            if ocean.grid[ny][nx] is None:
                empty_neighbors.append((nx, ny))
        
        # Si des cases vides sont disponibles, se déplacer
        if empty_neighbors:
            import random
            nx, ny = random.choice(empty_neighbors)
            
            # Vérifier si reproduction possible
            if self.reproduction_counter >= FISH_REPRODUCTION_TIME:
                # Laisser un nouveau poisson à l'ancienne position
                ocean.grid[self.y][self.x] = Sardine(self.x, self.y)
                self.reproduction_counter = 0
            else:
                # Sinon, laisser la case vide
                ocean.grid[self.y][self.x] = None
            
            # Déplacer le poisson
            self.x, self.y = nx, ny
            ocean.grid[ny][nx] = self
            return True
        
        return False

Fish = Sardine