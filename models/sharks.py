from models.fishes import Fish, Sardine
from models.utils.config import (
    SHARK_ENERGY_GAIN, 
    SHARK_STARVATION_TIME, 
    SHARK_REPRODUCTION_TIME
)

class Shark(Fish):
    """Classe représentant un requin, qui peut manger des sardines."""
    def __init__(self, x=0, y=0, age=0, shark_energy=SHARK_STARVATION_TIME):
        super().__init__(x, y, age)
        self.shark_energy = shark_energy
        self.shark_starvation_time = SHARK_STARVATION_TIME
        self.shark_reproduction_threshold = SHARK_REPRODUCTION_TIME
        self.shark_reproduction_counter = 0
    
    def age_up(self):
        """Incrémente l'âge et le compteur de reproduction du requin."""
        super().age_up()
        self.shark_reproduction_counter += 1
    
    def can_eat(self, entity):
        """Vérifie si l'entité peut être mangée par le requin."""
        return isinstance(entity, Sardine)
    
    def move(self, ocean):
        """Implémentation de la méthode abstraite de déplacement pour les requins."""
        # Vérifier d'abord si le requin a encore de l'énergie
        self.shark_energy -= 1
        if self.shark_energy <= 0:
            return False  # Le requin meurt de faim
        
        # Rechercher d'abord les sardines voisines à manger
        sardine_neighbors = []
        for nx, ny in ocean.get_neighbors(self.x, self.y):
            if isinstance(ocean.grid[ny][nx], Sardine):
                sardine_neighbors.append((nx, ny))
        
        # Si des sardines sont disponibles, en manger une
        if sardine_neighbors:
            import random
            nx, ny = random.choice(sardine_neighbors)
            
            # Manger la sardine et regagner de l'énergie
            self.shark_energy += SHARK_ENERGY_GAIN
            
            # Vérifier si reproduction possible
            if self.shark_reproduction_counter >= self.shark_reproduction_threshold:
                # Laisser un nouveau requin à l'ancienne position
                ocean.grid[self.y][self.x] = Shark(self.x, self.y)
                self.shark_reproduction_counter = 0
            else:
                # Sinon, laisser la case vide
                ocean.grid[self.y][self.x] = None
            
            # Déplacer le requin
            self.x, self.y = nx, ny
            ocean.grid[ny][nx] = self
            return True
        
        # Si pas de sardines à proximité, chercher une case vide
        empty_neighbors = []
        for nx, ny in ocean.get_neighbors(self.x, self.y):
            if ocean.grid[ny][nx] is None:
                empty_neighbors.append((nx, ny))
        
        # Si des cases vides sont disponibles, se déplacer
        if empty_neighbors:
            import random
            nx, ny = random.choice(empty_neighbors)
            
            # Vérifier si reproduction possible
            if self.shark_reproduction_counter >= self.shark_reproduction_threshold:
                # Laisser un nouveau requin à l'ancienne position
                ocean.grid[self.y][self.x] = Shark(self.x, self.y)
                self.shark_reproduction_counter = 0
            else:
                # Sinon, laisser la case vide
                ocean.grid[self.y][self.x] = None
            
            # Déplacer le requin
            self.x, self.y = nx, ny
            ocean.grid[ny][nx] = self
            return True
        
        # Si aucun mouvement n'est possible, rester sur place
        return False