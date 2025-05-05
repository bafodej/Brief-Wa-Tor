import time 
from ocean.ocean import Ocean

def main():
    # Créer l'océan et initialiser la simulation
    ocean = Ocean()  # La initialisation se fait dans le constructeur
    
    # Nombre d'étapes de simulation
    steps = 100
    
    # Pause entre les étapes (en secondes)
    pause_time = 0.5
    
    # Pour suivre les statistiques
    sardine_stats = []
    shark_stats = []
    
    print("Démarrage de la simulation Wa-Tor")
    print("---------------------------------")
    
    for step in range(steps):
        # Exécuter une étape de simulation
        sardine_count, shark_count = ocean.run_simulation_step()
        
        # Enregistrer les statistiques
        sardine_stats.append(sardine_count)
        shark_stats.append(shark_count)
        
        # Afficher l'état actuel
        print(f"Chronon {step+1}/{steps} - Sardines: {sardine_count}, Requins: {shark_count}")
        
        # Vérifier si l'une des populations est éteinte
        if sardine_count == 0 or shark_count == 0:
            print("Une espèce s'est éteinte, fin de la simulation.")
            break
        
        # Pause pour voir l'évolution
        time.sleep(pause_time)
    
    # Statistiques finales
    print("\nStatistiques finales:")
    print(f"Sardines: {sardine_stats[-1]}")
    print(f"Requins: {shark_stats[-1]}")

if __name__ == "__main__":
    main()