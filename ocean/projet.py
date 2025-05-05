
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

# --- Création d’une grille vide (océan) ---
Ocean: Grid = [[None for _ in range(width)] for _ in range(height)]

def initialize_ocean() -> None:
    """
    Remplit l'océan aléatoirement :
    - 90 % de poissons,
    - 5 % de requins,
    - 5 % d'eau.
    """
    for y in range(height):
        for x in range(width):
            r = random.random()
            if r < 0.9:
                Ocean[y][x] = Fish()
            elif r < 0.95:
                Ocean[y][x] = Shark()

def toroidal(x: int, y: int) -> Tuple[int, int]:
    """
    Gère les bords de la grille en mode torique :
    Si on sort à droite, on revient à gauche, etc.
    """
    return x % width, y % height

def get_neighbors(x: int, y: int) -> List[Tuple[int, int]]:
    """
    Retourne les coordonnées des 4 cellules voisines immédiates (haut, bas, gauche, droite).
    L’ordre est aléatoire pour éviter des biais de direction.
    """
    directions = [(-1,0), (1,0), (0,-1), (0,1)]
    neighbors = [toroidal(x + dx, y + dy) for dx, dy in directions]
    random.shuffle(neighbors)
    return neighbors

# --- Mise à jour de l'océan ---
def update_ocean() -> None:
    """
    Met à jour la grille :
    - Les sardines se déplacent et se reproduisent s’ils ont l’âge requis.
    - Les requins mangent les poissons, se déplacent, se reproduisent, ou meurent s’ils n’ont plus d’énergie.
    """
    global Ocean
    new_ocean: Grid = [[None for _ in range(width)] for _ in range(height)]
    has_moved = [[False for _ in range(width)] for _ in range(height)]

    for y in range(height):
        for x in range(width):
            entity = Ocean[y][x]
            if entity is None or has_moved[y][x]:
                continue

            if isinstance(entity, Fish):
                entity.age += 1
                moved = False
                for nx, ny in get_neighbors(x, y):
                    if Ocean[ny][nx] is None and new_ocean[ny][nx] is None:
                        # Reproduction
                        if entity.age >= fish_reproduction_time:
                            new_ocean[y][x] = Fish()
                            entity.age = 0
                        new_ocean[ny][nx] = Fish(age=entity.age)
                        has_moved[ny][nx] = True
                        moved = True
                        break
                if not moved:
                    new_ocean[y][x] = entity

            elif isinstance(entity, Shark):
                entity.age += 1
                entity.energy -= 1
                moved = False
                for nx, ny in get_neighbors(x, y):
                    # Le requin mange un poisson s’il en trouve un
                    if isinstance(Ocean[ny][nx], Fish) and new_ocean[ny][nx] is None:
                        new_shark = Shark(age=entity.age, energy=shark_energy)
                        if entity.age >= shark_reproduction_time:
                            new_ocean[y][x] = Shark()
                            new_shark.age = 0
                        new_ocean[ny][nx] = new_shark
                        has_moved[ny][nx] = True
                        moved = True
                        break

                if not moved:
                    # Sinon, il se déplace dans une case vide
                    for nx, ny in get_neighbors(x, y):
                        if Ocean[ny][nx] is None and new_ocean[ny][nx] is None:
                            new_shark = Shark(age=entity.age, energy=entity.energy)
                            if entity.age >= shark_reproduction_time:
                                new_ocean[y][x] = Shark()
                                new_shark.age = 0
                            new_ocean[ny][nx] = new_shark
                            has_moved[ny][nx] = True
                            moved = True
                            break

                # Si aucune action n’est possible, il reste sur place s’il est encore en vie
                if not moved and entity.energy > 0:
                    new_ocean[y][x] = entity

    Ocean = new_ocean

# --- Interface graphique Tkinter ---
class WaTorApp:
    """Classe principale Tkinter : dessine et anime la simulation dans une fenêtre."""
    def __init__(self, master: tk.Tk) -> None:
        self.master = master
        self.canvas = tk.Canvas(master, width=width * cell_size, height=height * cell_size, bg="#a3dfff")
        self.canvas.pack()
        
        ""      
        # Affichage du compteur de chronons
        self.counter_label = tk.Label(master, text="Chronon: 0", font=("Arial", 14))
        self.counter_label.pack()
        
        # Graphique du nombre de poissons et requins
        self.stats_label = tk.Label(master, text="Sardines: 0 | Requins: 0", font=("Arial", 14))
        self.stats_label.pack()

        # Bouton Play/Pause
        self.play_pause_button = tk.Button(master, text="Play", font=("Arial", 14), command=self.toggle_play_pause)
        self.play_pause_button.pack()

        self.counter = 0  # Initialisation du compteur de chronons
        self.is_running = False  # Variable de contrôle pour Play/Pause
        self.update_gui()
        
    def toggle_play_pause(self) -> None:
        """Alterne entre play et pause."""
        if self.is_running:
            self.is_running = False
            self.play_pause_button.config(text="Play")
        else:
            self.is_running = True
            self.play_pause_button.config(text="Pause")
            self.simulation_step()  # Démarre la simulation si elle n'est pas déjà en cours

    def update_gui(self) -> None:
        """
        Efface l'affichage précédent et redessine chaque entité à sa nouvelle position.
        Fond = bleu clair, emoji 🐟 = poisson, emoji 🦈 = requin.
        """
        self.canvas.delete("all")
        for y in range(height):
            for x in range(width):
                entity = Ocean[y][x]
                cx = x * cell_size + cell_size // 2  # Centre x
                cy = y * cell_size + cell_size // 2  # Centre y
                if isinstance(entity, Fish):
                    self.canvas.create_text(cx, cy, text="🐟", font=("Arial", int(cell_size / 1.5)))
                elif isinstance(entity, Shark):
                    self.canvas.create_text(cx, cy, text="🦈", font=("Arial", int(cell_size / 1.5)))
        
        # Mise à jour du compteur de chronons
        self.counter_label.config(text=f"Chronon: {self.counter}")
        
        # Mise à jour des statistiques des poissons et requins
        fish_count = sum(isinstance(cell, Fish) for row in Ocean for cell in row)
        shark_count = sum(isinstance(cell, Shark) for row in Ocean for cell in row)
        self.stats_label.config(text=f"Poissons: {fish_count} | Requins: {shark_count}")

    def simulation_step(self) -> None:
        """Avance d’un chronon : met à jour les entités et redessine la grille."""
        if not self.is_running:
            return  # Si la simulation est en pause, ne pas continuer

        self.counter += 1  # Incrémente le compteur de chronons
        update_ocean()
        self.update_gui()
        self.master.after(200, self.simulation_step)  # Boucle animée continue

# --- Point d'entrée du programme ---
def main() -> None:
    """Initialise la simulation et démarre l'interface graphique."""
    initialize_ocean()
    root = tk.Tk()
    root.title("Simulation Wa-Tor 🐟🦈")
    app = WaTorApp(root)
    root.mainloop()

# --- Lancement de l’application ---
if __name__ == "__main__":
    main()
    
# --- Fin du code ---