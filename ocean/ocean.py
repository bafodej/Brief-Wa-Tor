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