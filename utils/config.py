from models.sharks import Shark

def shark_reproduction_time(self, old_position, grille):
    if self.age >= self.shark_reproduction_time:
        bebe = Shark(...mêmes paramètres initiaux...)
        grille.set_case(old_position, bebe)
        self.age = 0