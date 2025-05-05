# Configuration de la simulation

# Unité de base de temps
CRONON = 4

# Probabilités d'apparition initiales
INITIAL_SARDINE_PROBABILITY = 0.2
INITIAL_SHARK_PROBABILITY = 0.1

# Configuration des organismes
# SARDINE_REPRODUCTION_TIME = 1Ò
SHARK_REPRODUCTION_TIME = 3
SHARK_INITIAL_ENERGY = 15
SHARK_STARVATION_TIME = 15

# Énergie gagnée par un requin en mangeant une sardine
SHARK_ENERGY_GAIN = 10

# Configuration de la grille
GRID_WIDTH = 50
GRID_HEIGHT = 50

# Paramètres pour l'interface Tkinter
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 650
CANVAS_WIDTH = 600
CANVAS_HEIGHT = 600
SIMULATION_SPEED = 200  # ms entre les étapes (plus petit = plus rapide)

# Couleurs pour l'interface
WATER_COLOR = "#0077be"  # Bleu océan
SARDINE_COLOR = "#00cc00"   # Vert pour les sardines
SHARK_COLOR = "#cc0000"  # Rouge pour les requins
TEXT_COLOR = "#000000"  # Noir pour le texte