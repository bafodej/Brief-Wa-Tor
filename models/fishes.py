import random
from typing import List, Tuple, Optional

class Fish:
    """Classe de base pour les espèces de poissons dans la simulation Wa-Tor."""
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

class Sardine(Fish):
    """Classe représentant une sardine, qui peut être mangée par les requins."""
    def __init__(self, x=0, y=0, age=0):
        super().__init__(x, y, age)
        # Spécificités des sardines si nécessaire
Fish = Sardine