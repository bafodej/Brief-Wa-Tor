import random
from utils.config import *
from models.fishes import *
from models.sharks import *

# Définition des dimensions de la grille 
width = 50
height = 50

# Définition des paramétres pour les poissons et requins 

fish_reproduction_time = 5    # Un poisson se reproduit après 5 tous
shark_reproduction_time = 3   # Un requin se reproduit après 3 tours 
shark_energy = 1              # Un requin meurt s'il ne mange pas pendant 1 tour


water = None


# Définition des classes

class Fish:
   def __init__(self):
       self.age = 0

class Shark:
   def __init__(self):
# Compter les chronons depuis la naissance des
       self.age = 0   
       self.energy = shark_energy
       
# Création de la grille vide OCEAN qui ne contient que de l'eau 
Ocean = [[water for i in range (width)] for i in range (height)]
 
# Placer aléatoirement des poissons et des requins dans la grille    
for x in range(width):
   for y in range(height):
       r = random.random()
      
       if r < 0.2:         
           Ocean [x][y] = Fish()  # probabilité d'avoir un poisson dans la grille : 20 %
           
       elif r < 0.3:       
           Ocean [x][y] = Shark() # probabilité d'avoir un requin dans la grille : 10 %

# Définition fonction pour retourner dans la grille lorsqu'on arrive au bord        
def toroidal (x,y):
   return x % width, y % height
  
def move_toroidal (x,y):
  # definition de la direction du mouvement : gauche, droite, haut, bas
   directions = [(-1, 0), (1, 0), (0, -1), (0, 1)] 
   neighbors = []
  
   for dx, dy in directions:
        # Utilisation du module pour faire réapparaitre un objet de l'autre coté s'il dépasse le bord de la grille
        nx, ny = toroidal(x + dx, y + dy)
        neighbors.append((nx, ny))
          
   return neighbors