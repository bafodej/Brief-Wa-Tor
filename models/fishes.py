from utils.config import *
from models.sharks import *
from ocean.ocean import *

class Fish:
    def __init__(self, x, y, age=0):
        self.x = x
        self.y = y
        self.age = age
        self.fish_reproduction_time = 0
        self.do_movement = False                                   # Pour éviter de déplacer deux fois le même poisson
    
    def age(self):
        self.age += 1
        self.fish_reproduction_time += 1
    
    def can_reproduced(self):
        return self.fish_reproduction_time >= REPRODUCTION_TIME_FISH
    
    def to_reproduced(self):                                        # La création du nouveau poisson sera gérée par la planète/océan
        self.fish_reproduction_time = 0
       
    
    def to_moov(self, ocean):
        if self.do_movement:
            return False
            
        
        neighbour_empty = ocean.empty_box_neighbour(self.x, self.y)  # Chercher les cases vides 
        
        if not neighbour_empty:                                      # Pas de déplacement possible
            return False  
        
        
        new_x, new_y = ocean.random_choice(neighbour_empty)           # Sélectionner une case vide au hasard
        
        
        have_to_reproduced = self.can_reproduced()                    # Vérifier si reproduction possible
        
        
        ocean.moov_fish(self.x, self.y, new_x, new_y)                 # Déplacer le poisson
        self.x, self.y = new_x, new_y
        
        
        if have_to_reproduced:                                         # Reproduire si nécessaire
            self.to_reproduced()
            ocean.add_fishes(self.x, self.y)
            
        self.do_movement = True
        return True