import random
from typing import List, Tuple, Optional
from models.fishes import Fish
from models.utils.config import (
    SHARK_ENERGY_GAIN, 
    SHARK_STARVATION_TIME, 
    SHARK_REPRODUCTION_TIME,
    SHARK_INITIAL_ENERGY
)

class Shark(Fish):
    """Classe représentant un requin dans la simulation Wa-Tor."""
    def __init__(self, x=0, y=0, age=0, energy=SHARK_INITIAL_ENERGY):
        super().__init__(x, y, age)
        self.energy = energy
    
    def update(self) -> None:
        """Met à jour l'état du requin pour un chronon."""
        if self.moved:  # Si déjà déplacé dans ce chronon
            self.moved = False
            return
        
        from models.ocean import Ocean  # Import ici pour éviter l'import circulaire
        
        # Recherche des cellules avec des poissons adjacents
        fish_cells = []
        for nx, ny in Ocean.get_adjacent_positions(self.x, self.y):
            entity = Ocean.get_cell(nx, ny)
            if isinstance(entity, Fish) and not isinstance(entity, Shark):
                fish_cells.append((nx, ny))
        
        # Diminution de l'énergie à chaque tour
        self.energy -= 1
        
        if self.energy <= 0:  # Mort par manque d'énergie
            Ocean.set_cell(self.x, self.y, None)
            return
        
        if fish_cells:  # Chasse aux poissons si disponibles
            new_x, new_y = random.choice(fish_cells)
            self.energy = SHARK_STARVATION_TIME  # Regain d'énergie après avoir mangé
            
            # Reproduction si assez de temps écoulé
            if self.breed_counter >= SHARK_REPRODUCTION_TIME:
                self.breed_counter = 0
                # Place un nouveau requin à l'ancienne position
                Ocean.set_cell(self.x, self.y, Shark(self.x, self.y))
            else:
                # Sinon, juste déplacer le requin
                Ocean.set_cell(self.x, self.y, None)
            
            # Mise à jour position et manger le poisson
            self.x, self.y = new_x, new_y
            Ocean.set_cell(self.x, self.y, self)
            self.breed_counter += 1
            self.moved = True
        else:
            # Recherche des cellules vides adjacentes si pas de poisson à manger
            empty_cells = []
            for nx, ny in Ocean.get_adjacent_positions(self.x, self.y):
                if Ocean.get_cell(nx, ny) is None:
                    empty_cells.append((nx, ny))
            
            if empty_cells:  # S'il y a des cellules vides
                new_x, new_y = random.choice(empty_cells)
                
                # Reproduction si assez de temps écoulé
                if self.breed_counter >= SHARK_REPRODUCTION_TIME:
                    self.breed_counter = 0
                    # Place un nouveau requin à l'ancienne position
                    Ocean.set_cell(self.x, self.y, Shark(self.x, self.y))
                else:
                    # Sinon, juste déplacer le requin
                    Ocean.set_cell(self.x, self.y, None)
                
                # Mise à jour position
                self.x, self.y = new_x, new_y
                Ocean.set_cell(self.x, self.y, self)
                self.breed_counter += 1
                self.moved = True