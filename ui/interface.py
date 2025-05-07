import tkinter as tk
from tkinter import ttk, messagebox
import time
import threading
from ocean.ocean import Ocean
from models.fishes import Sardine
from models.sharks import Shark
from models.utils.config import (
    GRID_WIDTH, GRID_HEIGHT, 
    INITIAL_SARDINE_PROBABILITY, INITIAL_SHARK_PROBABILITY
)

class WaTorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulation Wa-Tor")
        self.root.resizable(True, True)
        
        # Variables de configuration
        self.canvas_width = 25
        self.canvas_height = 25
        self.cell_size = min(self.canvas_width // GRID_WIDTH, self.canvas_height // GRID_HEIGHT)
        
        # Couleurs
        self.water_color = "#0077be"  # Bleu océan
        self.sardine_color = "#00cc00"   # Vert
        self.shark_color = "#cc0000"  # Rouge
        
        # Variables de contrôle
        self.running = False
        self.simulation_speed = 200  # ms entre les étapes (plus petit = plus rapide)
        self.cronon = 0  # Compteur de pas de simulation
        
        # Initialisation de l'océan
        self.ocean = Ocean(GRID_WIDTH, GRID_HEIGHT)
        self.sardine_count, self.shark_count = self.ocean.count_fish()  # 
        
        # Création de l'interface
        self.create_widgets()
        
        # Première mise à jour de l'affichage
        self.update_display()
        
    def create_widgets(self):
        # Frame principale
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Cadre pour le canvas (simulation)
        canvas_frame = ttk.Frame(main_frame, padding="5")
        canvas_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")
        
        # Canvas pour afficher la simulation
        self.canvas = tk.Canvas(canvas_frame, width=self.canvas_width, height=self.canvas_height, bg="black")
        self.canvas.pack(fill="both", expand=True)
        
        # Panneau de contrôle
        control_frame = ttk.Frame(main_frame, padding="5")
        control_frame.grid(row=0, column=1, sticky="nsew")
        
        # Statistiques
        stats_frame = ttk.LabelFrame(control_frame, text="Statistiques", padding="10")
        stats_frame.pack(fill="x", pady=5)
        
        self.cronon_var = tk.StringVar(value="Cronon: 0")
        self.sardine_var = tk.StringVar(value=f"Sardines: {self.sardine_count}")
        self.shark_var = tk.StringVar(value=f"Requins: {self.shark_count}")
        
        ttk.Label(stats_frame, textvariable=self.cronon_var).pack(anchor="w")
        ttk.Label(stats_frame, textvariable=self.sardine_var).pack(anchor="w")
        ttk.Label(stats_frame, textvariable=self.shark_var).pack(anchor="w")
        
        # Contrôles de simulation
        sim_frame = ttk.LabelFrame(control_frame, text="Contrôles", padding="10")
        sim_frame.pack(fill="x", pady=5)
        
        # Boutons
        self.start_button = ttk.Button(sim_frame, text="Démarrer", command=self.toggle_simulation)
        self.start_button.pack(fill="x", pady=2)
        
        self.step_button = ttk.Button(sim_frame, text="Un pas", command=self.step_simulation)
        self.step_button.pack(fill="x", pady=2)
        
        self.reset_button = ttk.Button(sim_frame, text="Réinitialiser", command=self.reset_simulation)
        self.reset_button.pack(fill="x", pady=2)
        
        # Vitesse de simulation
        speed_frame = ttk.Frame(sim_frame)
        speed_frame.pack(fill="x", pady=5)
        
        ttk.Label(speed_frame, text="Vitesse:").pack(side="left")
        self.speed_scale = ttk.Scale(
            speed_frame, 
            from_=50, 
            to=500, 
            orient="horizontal", 
            value=self.simulation_speed,
            command=self.set_speed
        )
        self.speed_scale.pack(side="right", fill="x", expand=True)
        
        # Légende
        legend_frame = ttk.LabelFrame(control_frame, text="Légende", padding="10")
        legend_frame.pack(fill="x", pady=5)
        
        sardine_legend = ttk.Frame(legend_frame)
        sardine_legend.pack(fill="x", pady=2)
        sardine_color = ttk.Label(sardine_legend, text="    ", background=self.sardine_color)
        sardine_color.pack(side="left")
        ttk.Label(sardine_legend, text=" Sardine 🐟").pack(side="left")
        
        shark_legend = ttk.Frame(legend_frame)
        shark_legend.pack(fill="x", pady=2)
        shark_color = ttk.Label(shark_legend, text="    ", background=self.shark_color)
        shark_color.pack(side="left")
        ttk.Label(shark_legend, text=" Requin 🦈").pack(side="left")
        
        water_legend = ttk.Frame(legend_frame)
        water_legend.pack(fill="x", pady=2)
        water_color = ttk.Label(water_legend, text="    ", background=self.water_color)
        water_color.pack(side="left")
        ttk.Label(water_legend, text=" Eau 🟦").pack(side="left")
        
        # Configurer les poids de la grille pour le redimensionnement
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=3)
        main_frame.grid_columnconfigure(1, weight=1)
    
    def update_display(self):
        # Effacer le canvas
        self.canvas.delete("all")

        self.canvas.create_rectangle(0, 0, self.canvas.winfo_width(), self.canvas.winfo_height(), fill=self.water_color, outline="")
        
        # Calculer la taille des cellules en fonction de la taille du canvas
        canvas_width = self.canvas.winfo_width() or self.canvas_width
        canvas_height = self.canvas.winfo_height() or self.canvas_height
        
        self.cell_size = min(
            canvas_width // self.ocean.width,
            canvas_height // self.ocean.height
        )
        
        if self.cell_size < 1:
            self.cell_size = 1  # Taille minimale

           # Emojis pour les organismes
        sardine_emoji = "🐟"  # Emoji poisson
        shark_emoji = "🦈"    # Emoji requin

            # Dessiner la grille
        for y in range(self.ocean.height):
            for x in range(self.ocean.width):
                organism = self.ocean.grid[y][x]
                
                # Coordonnées du centre de la cellule
                x_center = x * self.cell_size + self.cell_size // 2
                y_center = y * self.cell_size + self.cell_size // 2
                
                # Ajouter un emoji en fonction du type d'organisme
                if isinstance(organism, Sardine):
                    self.canvas.create_text(x_center, y_center, text=sardine_emoji, font=("Arial", self.cell_size // 2))
                elif isinstance(organism, Shark):
                    self.canvas.create_text(x_center, y_center, text=shark_emoji, font=("Arial", self.cell_size // 2))
        
        # Mettre à jour les statistiques
        self.cronon_var.set(f"Cronon: {self.cronon}")
        self.sardine_var.set(f"Sardines: {self.sardine_count}")
        self.shark_var.set(f"Requins: {self.shark_count}")
    
    def toggle_simulation(self):
            if self.running:
                self.running = False
                self.start_button.config(text="Démarrer")
            else:
                self.running = True
                self.start_button.config(text="Pause")
            # Lancer la simulation dans un thread pour ne pas bloquer l'interface
            threading.Thread(target=self.run_simulation, daemon=True).start()
    
    def run_simulation(self):
        while self.running:
            self.step_simulation()
            time.sleep(self.simulation_speed / 1000)  # Convertir ms en secondes
    
    def step_simulation(self):
        # Exécuter une seule étape de simulation
        self.sardine_count, self.shark_count = self.ocean.run_simulation_step()
        self.cronon += 1  # Incrémenter le compteur de cronons
        
        # Mettre à jour l'interface depuis le thread principal
        self.root.after(0, self.update_display)
        
        # Vérifier si la simulation est terminée
        if self.sardine_count == 0 or self.shark_count == 0:
            self.running = False
            self.root.after(0, self.show_end_message)
    
    def show_end_message(self):
        self.start_button.config(text="Démarrer")
        message = "Simulation terminée !\n"
        if self.sardine_count == 0 and self.shark_count == 0:
            message += "Tous les organismes ont disparu."
        elif self.sardine_count == 0:
            message += "Toutes les sardines ont été mangées. Les requins ont gagné !"
        else:
            message += "Tous les requins sont morts de faim. Les sardines ont gagné !"
        
        messagebox.showinfo("Fin de la simulation", message)
    
    def reset_simulation(self):
        # Arrêter la simulation en cours
        self.running = False
        self.start_button.config(text="Démarrer")
        
        # Réinitialiser l'océan et le compteur
        self.ocean = Ocean(GRID_WIDTH, GRID_HEIGHT)
        self.cronon = 0
        self.sardine_count, self.shark_count = self.ocean.count_fish()  # Corrigé ici
        
        # Mettre à jour l'affichage
        self.update_display()
    
    def set_speed(self, value):
        self.simulation_speed = float(value)

