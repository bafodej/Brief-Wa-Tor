# 🌊 Simulation Wa-Tor 🐟🦈 (Tkinter)

Simulation inspirée du monde de **Wa-Tor**, une planète peuplée de **sardines** et de **requins** évoluant dans un **océan torique**. Cette version utilise **Python avec Tkinter** pour l'affichage graphique.

## 📦 Contenu

- Simulation d'un écosystème sardine-requin
- Affichage animé avec émojis (🐟 et 🦈)
- Grille torique (rebords connectés)
- Bouton Play/Pause
- Statistiques en temps réel (nombre de poissons et de requins)

---

## ▶️ Comment exécuter le programme

1. **Prérequis** :
   - Python 3.12 ou supérieur
   - Aucun module externe requis (Tkinter est inclus avec Python standard)

2. **Lancer la simulation** :
   - Télécharger ou cloner le dépôt
   - Ouvrir un terminal et exécuter :

     ```bash
     python simulation_wator_tkinter.py
     ```

3. **Interface** :
   - Une fenêtre s’ouvre avec une mer bleue.
   - Cliquez sur **Play** pour démarrer la simulation, et **Pause** pour l'arrêter.
   - Les poissons (🐟) se déplacent et se reproduisent.
   - Les requins (🦈) chassent, se reproduisent ou meurent de faim.

---

## ⚙️ Paramètres de la simulation

| Paramètre                    | Valeur par défaut | Description                                                                 |
|-----------------------------|-------------------|-----------------------------------------------------------------------------|
| `width`                     | 25                | Largeur de la grille                                                       |
| `height`                    | 15                | Hauteur de la grille                                                       |
| `cell_size`                 | 30                | Taille d’affichage des cellules (en pixels)                               |
| `fish_reproduction_time`    | 9                 | Nombre de chronons avant reproduction d’un poisson                        |
| `shark_reproduction_time`   | 3                 | Nombre de chronons avant reproduction d’un requin                         |
| `shark_energy`              | 7                 | Énergie initiale d’un requin ; diminue chaque chronon, remonte en mangeant |

Ces paramètres peuvent être modifiés directement dans le fichier source (`simulation_wator_tkinter.py`) pour tester différents comportements écologiques.

---

## 👥 Équipe & Contributions

| Nom                   | Rôle                             | Contributions principales                                                |
|-----------------------|----------------------------------|-----------------------------------------------------------|
| Amina ABDEDDAÏM       | Définition de la grille          | Implémentation de la logique de simulation (Fish, Shark)|
| Amina ABDEDDAÏM       | Interface utilisateur            | Développement de l’interface Tkinter (affichage, bouton)      |
| Sophie Martin          | Tests et validation             | Tests du comportement, réglages des paramètres  |
| Karim Ouali            | Documentation & README          | Rédaction de la documentation, explication du modèle    |

---



