# Configuration de la simulation

# Unité de base de temps
CRONON = 4

# Probabilités d'apparition initiales
INITIAL_SARDINE_PROBABILITY = 0.2
INITIAL_SHARK_PROBABILITY = 0.1

# Configuration des organismes
FISH_REPRODUCTION_TIME = 8
SHARK_REPRODUCTION_TIME = 12
SHARK_INITIAL_ENERGY = 6
SHARK_STARVATION_TIME = 6

# Énergie gagnée par un requin en mangeant une sardine
SHARK_ENERGY_GAIN = 10

# Configuration de la grille
GRID_WIDTH = 25
GRID_HEIGHT = 25

# Paramètres pour l'interface Tkinter
WINDOW_WIDTH = 90
WINDOW_HEIGHT = 65
CANVAS_WIDTH = 600
CANVAS_HEIGHT = 600
SIMULATION_SPEED = 200  # ms entre les étapes (plus petit = plus rapide)

# Couleurs pour l'interface
WATER_COLOR = "#0077be"  # Bleu océan
SARDINE_COLOR = "#00cc00"   # Vert pour les sardines
SHARK_COLOR = "#cc0000"  # Rouge pour les requins
TEXT_COLOR = "#000000"  # Noir pour le texte