import utils.config
from utils.config import shark_reproduction_time

class Shark(Fish):
    def __init__(self, shark_energy, shark_starvation_time, shark_reproduction_time):
        super().__init__()  # si Poisson a des attributs à initier
        self.shark_energy = shark_energy
        self.shark_starvation_time = shark_starvation_time
        self.shark_reproduction_time = shark_reproduction_time
        self.age = 0  # utile pour reproduction



def move_shark(self, position, grille):
    self.age += 1
    self.shark_energy -= 1
    self.shark_reproduction_time += 1





