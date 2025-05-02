
import tkinter as tk      # Module pour créer l'interface graphique
import random             # Pour générer des positions et entités aléatoires

# --- Paramètres de la simulation ---
width = 25                # Largeur de la grille
height = 15               # Hauteur de la grille
cell_size = 30            # Taille visuelle de chaque cellule (en pixels)

fish_reproduction_time = 9        # Temps nécessaire avant qu'un poisson puisse se reproduire
shark_reproduction_time = 3       # Temps nécessaire avant qu'un requin puisse se reproduire
shark_energy = 7                  # Énergie initiale d’un requin
water = None                      # Représente une case vide (eau)
chronon = 1                       # Compteur de chronons (tours de simulation)

# --- Définition des classes pour les entités ---
class Fish:
    def __init__(self, age=0):
        self.age = age      # L'âge sert à déterminer la reproduction

class Shark:
    def __init__(self, age=0, energy=shark_energy):
        self.age = age
        self.energy = energy  # L'énergie du requin diminue à chaque tour

# --- Création de la grille toroïdale vide ---
Ocean = [[water for _ in range(width)] for _ in range(height)]

# --- Placement aléatoire des poissons et requins dans la grille ---
for y in range(height):
    for x in range(width):
        r = random.random()
        if r < 0.9:
            Ocean[y][x] = Fish()    # 90 % de chances de mettre un poisson
        elif r < 0.95:
            Ocean[y][x] = Shark()   # 5 % de chances de mettre un requin

# --- Fonction pour gérer les bords (grille toroïdale) ---
def toroidal(x, y):
    return x % width, y % height   # Permet de "boucler" les bords de la grille

# --- Récupération des voisins d’une cellule ---
def get_neighbors(x, y):
    directions = [(-1,0), (1,0), (0,-1), (0,1)]  # Deéfinition du déplacement : Gauche, droite, haut, bas
    neighbors = []
    for dx, dy in directions:
        nx, ny = toroidal(x + dx, y + dy)       # Position ajustée toroidalement
        neighbors.append((nx, ny))
    random.shuffle(neighbors)                   # Mélanger pour ajouter de l'aléatoire
    return neighbors

# --- Fonction de mise à jour de la grille à chaque tour (chronon) ---
def update_ocean():
    global Ocean
    new_ocean = [[None for _ in range(width)] for _ in range(height)]  # Grille temporaire
    has_moved = [[False for _ in range(width)] for _ in range(height)] # Empêche les doubles mouvements

    for y in range(height):
        for x in range(width):
            if Ocean[y][x] is None or has_moved[y][x]:
                continue

            entity = Ocean[y][x]

            # --- Comportement du poisson ---
            if isinstance(entity, Fish):
                entity.age += 1
                neighbors = get_neighbors(x, y)
                moved = False
                for nx, ny in neighbors:
                    if Ocean[ny][nx] is None and new_ocean[ny][nx] is None:
                        # Reproduction
                        if entity.age >= fish_reproduction_time:
                            new_ocean[y][x] = Fish()
                            entity.age = 0
                        else:
                            new_ocean[y][x] = None
                        new_ocean[ny][nx] = Fish(age=entity.age)
                        has_moved[ny][nx] = True
                        moved = True
                        break
                if not moved:
                    new_ocean[y][x] = entity

            # --- Comportement du requin ---
            elif isinstance(entity, Shark):
                entity.age += 1
                entity.energy -= 1
                neighbors = get_neighbors(x, y)
                moved = False

                # Cherche un poisson à manger
                for nx, ny in neighbors:
                    if isinstance(Ocean[ny][nx], Fish) and new_ocean[ny][nx] is None:
                        new_shark = Shark(age=entity.age, energy=shark_energy)  # Manger = énergie remise à neuf
                        if entity.age >= shark_reproduction_time:
                            new_ocean[y][x] = Shark()
                            new_shark.age = 0
                        else:
                            new_ocean[y][x] = None
                        new_ocean[ny][nx] = new_shark
                        has_moved[ny][nx] = True
                        moved = True
                        break

                # Sinon, essaye de se déplacer dans une case vide
                if not moved:
                    for nx, ny in neighbors:
                        if Ocean[ny][nx] is None and new_ocean[ny][nx] is None:
                            new_shark = Shark(age=entity.age, energy=entity.energy)
                            if entity.age >= shark_reproduction_time:
                                new_ocean[y][x] = Shark()
                                new_shark.age = 0
                            else:
                                new_ocean[y][x] = None
                            new_ocean[ny][nx] = new_shark
                            has_moved[ny][nx] = True
                            moved = True
                            break

                # Si le requin ne peut pas bouger, il reste sur place s'il a de l'énergie
                if not moved and entity.energy > 0:
                    new_ocean[y][x] = entity

    Ocean[:] = new_ocean  # Met à jour la grille principale avec la nouvelle

# --- Classe graphique avec Tkinter ---
class WaTorApp:
    def __init__(self, master):
        self.master = master
        # Création du canevas avec fond bleu clair
        self.canvas = tk.Canvas(master, width=width*cell_size, height=height*cell_size, bg="#a3dfff")
        self.canvas.pack()
        self.update_gui()
        self.master.after(200, self.simulation_step)  # Appel répété toutes les 200ms

    # Affichage graphique des entités
    def update_gui(self):
        self.canvas.delete("all")  # Efface tout à chaque frame
        for y in range(height):
            for x in range(width):
                entity = Ocean[y][x]
                x1 = x * cell_size + cell_size // 2
                y1 = y * cell_size + cell_size // 2
                if isinstance(entity, Fish):
                    self.canvas.create_text(x1, y1, text="🐟", font=("Arial", int(cell_size/1.5)))
                elif isinstance(entity, Shark):
                    self.canvas.create_text(x1, y1, text="🦈", font=("Arial", int(cell_size/1.5)))

    # Une étape de simulation (mise à jour + affichage)
    def simulation_step(self):
        update_ocean()      # Met à jour la grille
        self.update_gui()   # Met à jour l'affichage
        self.master.after(200, self.simulation_step)  # Boucle

# --- Lancement de l'application Tkinter ---
root = tk.Tk()
root.title("Wa-Tor 🐟🦈 - Océan Toroïdal")
app = WaTorApp(root)
root.mainloop()
