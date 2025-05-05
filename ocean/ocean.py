<<<<<<< HEAD
import tkinter as tk
import random
from typing import Optional, List, Tuple, Union  # Définition des types de valeur pour la simulation, Optinal (str) pour les entités vides, List [int] pour les listes, Tuple [str,int] pour les coordonnées x et y, Union [int,str] pour les entités (poisson ou requin). 

# --- Paramètres de la simulation ---
width = 25                     # Nombre de colonnes dans la grille
height = 15                    # Nombre de lignes dans la grille
cell_size = 30                 # Taille (pixels) de chaque cellule à l'écran

fish_reproduction_time = 9     # Nombre de chronons avant que le poisson se reproduise
shark_reproduction_time = 3    # Nombre de chronons avant que le requin se reproduise
shark_energy = 7               # Énergie de départ des requins

# --- Types utilisés dans la simulation ---
Entity = Union['Fish', 'Shark', None]  # Une cellule peut contenir un poisson, un requin ou être vide
Grid = List[List[Optional[Entity]]]    # Représentation de l’océan comme une grille 2D

# --- Définition des entités biologiques ---
class Fish:
    """Représente un poisson, avec un âge pour la reproduction."""
    def __init__(self, age: int = 0) -> None:
        self.age = age

class Shark:
    """Représente un requin, avec âge et énergie pour la survie et la reproduction."""
    def __init__(self, age: int = 0, energy: int = shark_energy) -> None:
        self.age = age
        self.energy = energy

class Ocean:
    """
    Classe représentant l'océan comme une grille 2D.
    Chaque cellule peut contenir un poisson, un requin ou être vide.
    """
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.grid: Grid = [[None for _ in range(width)] for _ in range(height)]
        self.initialize_ocean()
        
    def toroidal(self, x: int, y: int) -> Tuple[int, int]:
        """
        Gère les bords de la grille en mode torique :
        Si on sort à droite, on revient à gauche, etc.
        """
        return x % self.width, y % self.height
    
    def get_neighbors(self, x: int, y: int) -> List[Tuple[int, int]]:
        """
        Retourne les coordonnées des 4 cellules voisines immédiates (haut, bas, gauche, droite).
        """
        directions = [(-1,0), (1,0), (0,-1), (0,1)]
        neighbors = [self.toroidal(x + dx, y + dy) for dx, dy in directions]
        random.shuffle(neighbors)
        return neighbors
    
# --- Création d’une grille vide (océan) ---

def initialize_ocean(self) -> None:
    """
    Remplit l'océan aléatoirement :
    - 90 % de poissons,
    - 5 % de requins,
    - 5 % d'eau.
    """
    for y in range(self.height):
        for x in range(self.width):
            r = random.random()
            if r < 0.9:
                self.grid[y][x] = Fish()
            elif r < 0.95:
                self.grid[y][x] = Shark()
            else:
                self.grid[y][x] = None
                
    def print_ocean(self) -> None:
        """
        Affiche une représentation texte de l’océan pour débogage.
        """
        for row in self.grid:
            print(''.join(
                'S' if isinstance(cell, Shark) else
                'F' if isinstance(cell, Fish) else
                '.' for cell in row
            ))
    # --- Exemple d’utilisation ---
if __name__ == "__main__":
    ocean = Ocean(width=width, height=height)
    ocean.initialize()
    ocean.print_ocean()



# Fin du code
=======
import random
from models.fishes import Fish
from models.utils.config import (
    GRID_WIDTH, GRID_HEIGHT, 
    INITIAL_SARDINE_PROBABILITY, INITIAL_SHARK_PROBABILITY,
    SARDINE_REPRODUCTION_TIME, SHARK_REPRODUCTION_TIME,
    SHARK_INITIAL_ENERGY, SHARK_STARVATION_TIME
)

class Ocean:
    def __init__(self, width=GRID_WIDTH, height=GRID_HEIGHT):
        self.width = width
        self.height = height
        self.grid = [[None for _ in range(width)] for _ in range(height)]
        self.cronon = 0  # Compteur de pas de simulation
        self.initialize_grid()
    
    def initialize_grid(self):
        # Import ici pour éviter les importations circulaires
        from models.fishes import Sardine
        from models.sharks import Shark
        
        # Initialiser les compteurs ici
        shark_count = 0
        sardine_count = 0
        
        for x in range(self.width):
            for y in range(self.height):
                r = random.random()
                
                if r < INITIAL_SARDINE_PROBABILITY:
                    self.grid[y][x] = Sardine(x, y)
                    sardine_count += 1
                elif r < INITIAL_SARDINE_PROBABILITY + INITIAL_SHARK_PROBABILITY:
                    self.grid[y][x] = Shark(
                        x, y, 
                        shark_energy=SHARK_INITIAL_ENERGY,
                        shark_starvation_time=SHARK_STARVATION_TIME,
                        shark_reproduction_time=SHARK_REPRODUCTION_TIME
                    )
                    shark_count += 1
        
        print(f"Initialisation: {sardine_count} sardines, {shark_count} requins")
    
    def toroidal(self, x, y):
        """Implémente le toroïde pour que les bords de la grille se rejoignent"""
        return x % self.width, y % self.height
    
    def get_neighbors(self, x, y):
        """Obtient les coordonnées des cases voisines"""
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        neighbors = []
        
        for dx, dy in directions:
            nx, ny = self.toroidal(x + dx, y + dy)
            neighbors.append((nx, ny))
            
        return neighbors
    
    def empty_box_neighbour(self, x, y):
        """Trouve les cases voisines vides"""
        neighbors = self.get_neighbors(x, y)
        return [(nx, ny) for nx, ny in neighbors if self.grid[ny][nx] is None]
    
    def fish_neighbour(self, x, y):
        """Trouve les sardines voisines pour les requins"""
        from models.fishes import Sardine
        
        neighbors = self.get_neighbors(x, y)
        return [(nx, ny) for nx, ny in neighbors 
               if isinstance(self.grid[ny][nx], Sardine)]
    
    def random_choice(self, options):
        """Choix aléatoire parmi les options disponibles"""
        if not options:  # Protection contre liste vide
            return None, None
        return random.choice(options)
    
    def moov_fish(self, old_x, old_y, new_x, new_y):
        """Déplace un poisson d'une case à une autre"""
        self.grid[new_y][new_x] = self.grid[old_y][old_x]
        self.grid[old_y][old_x] = None
    
    def eat_fish(self, shark_x, shark_y, fish_x, fish_y):
        """Requin mange un poisson"""
        self.grid[fish_y][fish_x] = self.grid[shark_y][shark_x]
        self.grid[shark_y][shark_x] = None
    
    def add_fish(self, x, y, fish_class):
        """Ajoute un nouveau poisson (reproduction)"""
        # Trouver une case vide à proximité
        empty_neighbors = self.empty_box_neighbour(x, y)
        if empty_neighbors:
            nx, ny = self.random_choice(empty_neighbors)
            if nx is not None and ny is not None:
                # Créer une nouvelle instance de la classe de poisson appropriée
                self.grid[ny][nx] = fish_class(nx, ny)
    
    def remove_fish(self, x, y):
        """Supprime un poisson (mort)"""
        self.grid[y][x] = None
    
    def count_fish(self):
        """Compte le nombre de sardines et de requins"""
        from models.fishes import Sardine
        from models.sharks import Shark
        
        sardine_count = 0
        shark_count = 0
        
        for y in range(self.height):
            for x in range(self.width):
                fish = self.grid[y][x]
                if isinstance(fish, Sardine):
                    sardine_count += 1
                elif isinstance(fish, Shark):
                    shark_count += 1
        
        return sardine_count, shark_count
    
    def run_simulation_step(self):
        """Exécute une étape de la simulation"""
        from models.sharks import Shark
        from models.fishes import Sardine
        
        self.cronon += 1
        
        # Comptage avant mouvement pour débogage
        sardine_count, shark_count = self.count_fish()
        print(f"Début du chronon {self.cronon} - Sardines: {sardine_count}, Requins: {shark_count}")
        
        # Réinitialiser le flag do_movement et faire vieillir tous les poissons
        for y in range(self.height):
            for x in range(self.width):
                fish = self.grid[y][x]
                if isinstance(fish, Fish):  # Fish est la classe parente de Sardine et Shark
                    fish.do_movement = False
                    fish.age_up()
        
        # Déplacer tous les poissons
        for y in range(self.height):
            for x in range(self.width):
                fish = self.grid[y][x]
                
                if fish is None or fish.do_movement:
                    continue
                
                if isinstance(fish, Shark):
                    fish.move_shark(self)
                    fish.check_survival(self)
                elif isinstance(fish, Sardine):
                    fish.to_move(self)
        
        # Retourne les statistiques de l'étape
        return self.count_fish()
>>>>>>> ec582a9c1930c2d5c63eb99c04a897739c507553
