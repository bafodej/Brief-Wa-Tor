import tkinter as tk
from Ocean.ocean import initialize_ocean, update_ocean, toroidal, get_neighbors, width, height, cell_size, Fish, Shark, Ocean

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