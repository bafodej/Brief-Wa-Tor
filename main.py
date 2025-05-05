from ui import WaTorApp  # Importation de la classe principale Tkinter
import tkinter as tk  # Importation de la bibliothèque Tkinter
import random  # Importation de la bibliothèque random pour la génération aléatoire
from typing import Optional, List, Tuple, Union  # Importation des types pour la simulation
# --- Paramètres de la simulation ---
from ui import toggle_play_pause,update_gui, simulation_step, main  # Importation de la classe de l'interface
from ocean import initialize_ocean  # Importation de la fonction pour initialiser l'océan

def main() -> None:
  #  """Initialise la simulation et démarre l'interface graphique."""
  #  initialize_ocean()  # Initialiser l'océan avec des poissons et des requins
  #  root = tk.Tk()  # Création de la fenêtre Tkinter
    root.title("Simulation Wa-Tor 🐟🦈")  # Titre de la fenêtre
    app = WaTorApp(root)  # Création de l'application Tkinter
    root.mainloop()  # Démarrer la boucle Tkinter pour afficher l'interface

# --- Lancement de l’application ---
if __name__ == "__main__":
    main()
