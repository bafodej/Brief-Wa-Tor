import random
from typing import List, Tuple, Optional, Union
from models.fishes import Sardine
from models.sharks import Shark
from models.utils.config import (
    FISH_REPRODUCTION_TIME, 
    SHARK_REPRODUCTION_TIME,
    SHARK_STARVATION_TIME,
    INITIAL_SARDINE_PROBABILITY, 
    INITIAL_SHARK_PROBABILITY
)

class Ocean:
    """Classe qui gère l'océan et la simulation."""
    
    def __init__(self, width, height):
        """Initialise un océan avec les dimensions spécifiées."""
        self.width = width
        self.height = height
        self.grid = [[None for _ in range(width)] for _ in range(height)]
        self.initialize_grid()
    
    def initialize_grid(self):
        """Remplit la grille aléatoirement avec des sardines et des requins."""
        for y in range(self.height):
            for x in range(self.width):
                r = random.random()
                if r < INITIAL_SARDINE_PROBABILITY:
                    self.grid[y][x] = Sardine(x, y)
                elif r < INITIAL_SARDINE_PROBABILITY + INITIAL_SHARK_PROBABILITY:
                    self.grid[y][x] = Shark(x, y)
    
    def toroidal(self, x, y):
        """Gère les bords de la grille en mode torique."""
        return x % self.width, y % self.height
    
    def get_neighbors(self, x, y):
        """Retourne les coordonnées des 4 cellules voisines immédiates."""
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        neighbors = [self.toroidal(x + dx, y + dy) for dx, dy in directions]
        random.shuffle(neighbors)
        return neighbors
    
    def count_fish(self):
        """Compte le nombre de sardines et de requins dans l'océan."""
        sardine_count = 0
        shark_count = 0
        for y in range(self.height):
            for x in range(self.width):
                if isinstance(self.grid[y][x], Sardine) and not isinstance(self.grid[y][x], Shark):
                    sardine_count += 1
                elif isinstance(self.grid[y][x], Shark):
                    shark_count += 1
        return sardine_count, shark_count
    
    def run_simulation_step(self):
        """Exécute une étape de la simulation."""
        new_grid = [[None for _ in range(self.width)] for _ in range(self.height)]
        has_moved = [[False for _ in range(self.width)] for _ in range(self.height)]

        # Mettre à jour les requins d'abord
        for y in range(self.height):
            for x in range(self.width):
                entity = self.grid[y][x]
                if entity is None or has_moved[y][x]:
                    continue

                if isinstance(entity, Shark):
                    entity.age_up()
                    entity.shark_energy -= 1
                    moved = False
                    
                    # Si le requin n'a plus d'énergie, il meurt
                    if entity.shark_energy <= 0:
                        continue
                    
                    # Le requin cherche des sardines à manger
                    for nx, ny in self.get_neighbors(x, y):
                        if isinstance(self.grid[ny][nx], Sardine) and not isinstance(self.grid[ny][nx], Shark) and new_grid[ny][nx] is None:
                            # Le requin mange une sardine et regagne de l'énergie
                            entity.shark_energy = SHARK_STARVATION_TIME
                            
                            # Vérifier si reproduction possible
                            if entity.shark_reproduction_counter >= SHARK_REPRODUCTION_TIME:
                                new_grid[y][x] = Shark(x, y)
                                entity.shark_reproduction_counter = 0
                            
                            # Déplacer le requin à la position de la sardine
                            entity.x, entity.y = nx, ny
                            new_grid[ny][nx] = entity
                            has_moved[ny][nx] = True
                            moved = True
                            break
                    
                    if not moved:
                        # Sinon, il se déplace dans une case vide
                        for nx, ny in self.get_neighbors(x, y):
                            if self.grid[ny][nx] is None and new_grid[ny][nx] is None:
                                # Vérifier si reproduction possible
                                if entity.shark_reproduction_counter >= SHARK_REPRODUCTION_TIME:
                                    new_grid[y][x] = Shark(x, y)
                                    entity.shark_reproduction_counter = 0
                                
                                # Déplacer le requin
                                entity.x, entity.y = nx, ny
                                new_grid[ny][nx] = entity
                                has_moved[ny][nx] = True
                                moved = True
                                break
                    
                    # Si aucune action n'est possible, il reste sur place
                    if not moved:
                        new_grid[y][x] = entity

        # Ensuite mettre à jour les sardines
        for y in range(self.height):
            for x in range(self.width):
                entity = self.grid[y][x]
                if entity is None or has_moved[y][x]:
                    continue

                if isinstance(entity, Sardine) and not isinstance(entity, Shark):
                    entity.age_up()
                    moved = False
                    
                    for nx, ny in self.get_neighbors(x, y):
                        if self.grid[ny][nx] is None and new_grid[ny][nx] is None:
                            # Vérifier si reproduction possible
                            if entity.reproduction_counter >= FISH_REPRODUCTION_TIME:
                                new_grid[y][x] = Sardine(x, y)
                                entity.reproduction_counter = 0
                            
                            # Déplacer la sardine
                            entity.x, entity.y = nx, ny
                            new_grid[ny][nx] = entity
                            has_moved[ny][nx] = True
                            moved = True
                            break
                    
                    if not moved:
                        new_grid[y][x] = entity

        self.grid = new_grid
        return self.count_fish()