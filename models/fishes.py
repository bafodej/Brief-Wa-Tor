# Constants (déplacées depuis config.py)
CRONON = 12
FISH_REPRODUCTION_TIME = CRONON * 2

class Fish:
    """Classe de base pour les espèces de poissons dans la simulation Wa-Tor."""
    def __init__(self, x=0, y=0, age=0):
        self.x = x
        self.y = y
        self.age = age
        self.fish_reproduction_time = 0
        self.do_movement = False  # Pour éviter de déplacer deux fois le même organisme
    
    def age_up(self):
        """Méthode qui incrémente l'âge et le compteur de reproduction."""
        self.age += 1
        self.fish_reproduction_time += 1
    
    def can_reproduced(self):
        """Méthode qui vérifie si le poisson peut se reproduire"""
        return self.fish_reproduction_time >= FISH_REPRODUCTION_TIME
    
    def to_reproduced(self):
        """Initialisation de "l'age" de reproduction a 0"""
        self.fish_reproduction_time = 0
    
    def to_move(self, ocean):
        """Initialisation de la varible to_move a false"""
        if self.do_movement:
            return False
        """Verifie si la case voisine est vide, si la case n'est pas vide le poisson ne s'y déplace pas"""
        neighbour_empty = ocean.empty_box_neighbour(self.x, self.y)
        
        if not neighbour_empty:
            return False
        """Déplacement du poisson sur une case vide aléatoire et vérifie si peut se reproduire"""
        new_x, new_y = ocean.random_choice(neighbour_empty)
        
        have_to_reproduced = self.can_reproduced()
        
        ocean.moov_fish(self.x, self.y, new_x, new_y)
        self.x, self.y = new_x, new_y
        """Si il peut se reproduire , laisse derriere lui un poisson puis se déplace"""
        if have_to_reproduced:
            self.to_reproduced()
            ocean.add_fish(self.x, self.y, self.__class__)
            
        self.do_movement = True
        return True

class Sardine(Fish):
    """Classe représentant une sardine, qui peut être mangée par les requins."""
    def __init__(self, x=0, y=0, age=0):
        super().__init__(x, y, age)