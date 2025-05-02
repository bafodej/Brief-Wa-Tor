import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import random

# Paramètres de la grille

width = 25
height = 15
fish_reproduction_time = 10
shark_reproduction_time = 9
shark_energy = 2
water = None
chronon = 1


# Définition des classes 

class Fish:
    def __init__(self, age=0):
        self.age = age

class Shark:
    def __init__(self, age=0, energy=shark_energy):
        self.age = age
        self.energy = energy

# Grille toroïdale vide

Ocean = [[water for _ in range(width)] for _ in range(height)]

# Initialisation aléatoire de la grille

for y in range(height):
    for x in range(width):
        r = random.random()
        if r < 0.9:
            Ocean[y][x] = Fish()
        elif r < 0.95:
            Ocean[y][x] = Shark()


# Fonction pour retourner dans la grille lorsqu'on arrive au bord 

def toroidal(x, y):
    return x % width, y % height
# Définition des directions de mouvement : gauche, droite, haut, bas
def get_neighbors(x, y):
    directions = [(-1,0), (1,0), (0,-1), (0,1)]
    neighbors = []
    for dx, dy in directions:
        nx, ny = toroidal(x + dx, y + dy)
        neighbors.append((nx, ny))
    random.shuffle(neighbors)
    return neighbors

# Mise à jour de l'océan
def update_ocean():
    global Ocean
    new_ocean = [[None for _ in range(width)] for _ in range(height)]
    has_moved = [[False for _ in range(width)] for _ in range(height)]

    for y in range(height):
        for x in range(width):
            if Ocean[y][x] is None or has_moved[y][x]:
                continue

            entity = Ocean[y][x]

            if isinstance(entity, Fish):
                entity.age += 1
                neighbors = get_neighbors(x, y)
                moved = False
                for nx, ny in neighbors:
                    if Ocean[ny][nx] is None and new_ocean[ny][nx] is None:
                        # Reproduction
                        if entity.age >= fish_reproduction_time:
                            new_ocean[y][x] = Fish()  # Laisser un bébé
                            entity.age = 0
                        else:
                            new_ocean[y][x] = None
                        new_ocean[ny][nx] = Fish(age=entity.age)
                        has_moved[ny][nx] = True
                        moved = True
                        break
                if not moved:
                    new_ocean[y][x] = entity

            elif isinstance(entity, Shark):
                entity.age += 1
                entity.energy -= 1
                neighbors = get_neighbors(x, y)
                moved = False

                # Chercher un poisson à manger
                for nx, ny in neighbors:
                    if isinstance(Ocean[ny][nx], Fish) and new_ocean[ny][nx] is None:
                        new_shark = Shark(age=entity.age, energy=shark_energy)
                        # Reproduction
                        if entity.age >= shark_reproduction_time:
                            new_ocean[y][x] = Shark()
                            new_shark.age = 0
                        else:
                            new_ocean[y][x] = None
                        new_ocean[ny][nx] = new_shark
                        has_moved[ny][nx] = True
                        moved = True
                        break

                if not moved:
                    for nx, ny in neighbors:
                        if Ocean[ny][nx] is None and new_ocean[ny][nx] is None:
                            new_shark = Shark(age=entity.age, energy=entity.energy)
                            # Reproduction
                            if entity.age >= shark_reproduction_time:
                                new_ocean[y][x] = Shark()
                                new_shark.age = 0
                            else:
                                new_ocean[y][x] = None
                            new_ocean[ny][nx] = new_shark
                            has_moved[ny][nx] = True
                            moved = True
                            break

                if not moved and entity.energy > 0:
                    new_ocean[y][x] = entity

    Ocean[:] = new_ocean

# Affichage graphique
def draw_ocean():
    image = np.zeros((height, width, 3))
    for y in range(height):
        for x in range(width):
            cell = Ocean[y][x]
            if isinstance(cell, Fish):
                image[y][x] = [0.0, 1.0, 0.0]      # Vert
            elif isinstance(cell, Shark):
                image[y][x] = [1.0, 0.0, 0.0]      # Rouge
            else:
                image[y][x] = [0.6, 0.85, 1.0]     # Bleu clair
    return image

# Animation
fig, ax = plt.subplots()
ax.axis('off')
im = ax.imshow(draw_ocean(), interpolation='none')

def animate(frame):
    update_ocean()
    im.set_data(draw_ocean())
    return [im]

ani = animation.FuncAnimation(fig, animate, frames=200, interval=200, blit=True)
plt.show()
