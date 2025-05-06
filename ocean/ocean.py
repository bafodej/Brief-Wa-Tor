import random
from typing import List, Tuple, Optional, Union, Type

# Type pour la grille océanique
Grid = List[List[Optional[Union['Fish', 'Sardine', 'Shark', None]]]]

# Importation des classes et constantes
from models.fishes import Fish, Sardine
from models.sharks import Shark
from models.utils.config import (
    GRID_WIDTH, GRID_HEIGHT, 
    INITIAL_SARDINE_PROBABILITY, INITIAL_SHARK_PROBABILITY,
    FISH_REPRODUCTION_TIME, SHARK_REPRODUCTION_TIME,
    SHARK_INITIAL_ENERGY, SHARK_STARVATION_TIME,
    SHARK_ENERGY_GAIN
)

# Pour compatibilité avec main_tkinter
width = GRID_WIDTH
height = GRID_HEIGHT

# --- Création d'une grille vide (océan) ---
Ocean: Grid = [[None for _ in range(width)] for _ in range(height)]

def initialize_ocean() -> None:
    """
    Remplit l'océan aléatoirement :
    - 90 % de sardines,
    - 5 % de requins,
    - 5 % d'eau.
    """
    for y in range(height):
        for x in range(width):
            r = random.random()
            if r < INITIAL_SARDINE_PROBABILITY:
                Ocean[y][x] = Sardine(x, y)
            elif r < INITIAL_SARDINE_PROBABILITY + INITIAL_SHARK_PROBABILITY:
                Ocean[y][x] = Shark(x, y)
            else:
                Ocean[y][x] = None

def toroidal(x: int, y: int) -> Tuple[int, int]:
    """
    Gère les bords de la grille en mode torique :
    Si on sort à droite, on revient à gauche, etc.
    """
    return x % width, y % height

def get_neighbors(x: int, y: int) -> List[Tuple[int, int]]:
    """
    Retourne les coordonnées des 4 cellules voisines immédiates (haut, bas, gauche, droite).
    L'ordre est aléatoire pour éviter des biais de direction.
    """
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    neighbors = [toroidal(x + dx, y + dy) for dx, dy in directions]
    random.shuffle(neighbors)
    return neighbors

def update_ocean() -> None:
    """
    Met à jour la grille :
    - Les sardines se déplacent et se reproduisent s'ils ont l'âge requis.
    - Les requins mangent les sardines, se déplacent, se reproduisent, ou meurent s'ils n'ont plus d'énergie.
    """
    global Ocean
    new_ocean: Grid = [[None for _ in range(width)] for _ in range(height)]
    has_moved = [[False for _ in range(width)] for _ in range(height)]

    # Mettre à jour les requins d'abord (ils ont la priorité)
    for y in range(height):
        for x in range(width):
            entity = Ocean[y][x]
            if entity is None or has_moved[y][x]:
                continue

            if isinstance(entity, Shark):
                entity.age_up()
                entity.shark_energy -= 1
                moved = False
                
                # Le requin cherche des sardines à manger
                for nx, ny in get_neighbors(x, y):
                    if entity.can_eat(Ocean[ny][nx]) and new_ocean[ny][nx] is None:
                        # Le requin mange une sardine et regagne de l'énergie
                        entity.shark_energy += SHARK_ENERGY_GAIN
                        
                        # Vérifier si reproduction possible
                        if entity.shark_reproduction_counter >= SHARK_REPRODUCTION_TIME:
                            new_ocean[y][x] = Shark(x, y)
                            entity.shark_reproduction_counter = 0
                        
                        # Déplacer le requin à la position de la sardine
                        new_ocean[ny][nx] = entity
                        has_moved[ny][nx] = True
                        moved = True
                        break
                
                if not moved:
                    # Sinon, il se déplace dans une case vide
                    for nx, ny in get_neighbors(x, y):
                        if Ocean[ny][nx] is None and new_ocean[ny][nx] is None:
                            # Vérifier si reproduction possible
                            if entity.shark_reproduction_counter >= SHARK_REPRODUCTION_TIME:
                                new_ocean[y][x] = Shark(x, y)
                                entity.shark_reproduction_counter = 0
                            
                            # Déplacer le requin
                            new_ocean[ny][nx] = entity
                            has_moved[ny][nx] = True
                            moved = True
                            break
                
                # Si aucune action n'est possible, il reste sur place s'il est encore en vie
                if not moved and entity.shark_energy > 0:
                    new_ocean[y][x] = entity

    # Ensuite mettre à jour les sardines
    for y in range(height):
        for x in range(width):
            entity = Ocean[y][x]
            if entity is None or has_moved[y][x]:
                continue

            if isinstance(entity, Sardine):
                entity.age_up()
                moved = False
                
                for nx, ny in get_neighbors(x, y):
                    if Ocean[ny][nx] is None and new_ocean[ny][nx] is None:
                        # Vérifier si reproduction possible
                        if entity.reproduction_counter >= FISH_REPRODUCTION_TIME:
                            new_ocean[y][x] = Sardine(x, y)
                            entity.reproduction_counter = 0
                        
                        # Déplacer la sardine
                        new_ocean[ny][nx] = entity
                        has_moved[ny][nx] = True
                        moved = True
                        break
                
                if not moved:
                    new_ocean[y][x] = entity

    Ocean = new_ocean