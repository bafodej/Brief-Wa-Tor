import time 
from ocean.ocean import Ocean

# main.py (fichier principal à la racine du projet)

# Imports nécessaires
import tkinter as tk
from ui.interface import WaTorApp

def main():
    """Fonction principale qui lance l'application Wa-Tor."""
    # Créer la fenêtre principale
    root = tk.Tk()
    app = WaTorApp(root)
    
    # Configurer la taille initiale
    root.geometry("900x650")
    
    # Configurer le comportement lors du redimensionnement
    def on_resize(event):
        if event.widget == root:
            app.update_display()
    
    root.bind("<Configure>", on_resize)
    
    # Lancer l'interface
    root.mainloop()

if __name__ == "__main__":
    main()