 
from models.sharks import Shark

def shark_reproduction_time(self, old_position, grille):
    if self.age >= self.shark_reproduction_time:
        bebe = Shark(à définir)
        grille.set_case(old_position, bebe)
        self.age = 0

        
        
        
cronon = 12  # Déclaration du nombre de cronon
REPRODUCTION_TIME_FISH = cronon * 2
