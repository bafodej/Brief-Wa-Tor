from models.fishes import Fish
from models.utils.config import (
    SHARK_ENERGY_GAIN, SHARK_STARVATION_TIME, SHARK_REPRODUCTION_TIME
)

class Shark(Fish):
    def __init__(self, x=0, y=0, age=0, shark_energy=6, shark_starvation_time=6, shark_reproduction_time=12):
        super().__init__(x, y, age)
        self.shark_energy = shark_energy
        self.shark_starvation_time = shark_starvation_time
        self.shark_reproduction_threshold = shark_reproduction_time
        self.shark_reproduction_counter = 0
    
    def age_up(self):
        super().age_up()
        self.shark_reproduction_counter += 1
    
    def move_shark(self, ocean):
        if self.do_movement:
            return False
        
        # Vérifie s'il y a des sardines à proximité pour manger
        neighbor_sardines = ocean.sardine_neighbour(self.x, self.y)
        
        if neighbor_sardines:
            # Manger une sardine et gagner de l'énergie
            sardine_x, sardine_y = ocean.random_choice(neighbor_sardines)
            if sardine_x is not None and sardine_y is not None:
                ocean.eat_sardine(self.x, self.y, sardine_x, sardine_y)
                self.x, self.y = sardine_x, sardine_y
                self.shark_energy += SHARK_ENERGY_GAIN
                
                # Vérifier si reproduction possible
                if self.shark_reproduction_counter >= self.shark_reproduction_threshold:
                    ocean.add_shark(self.x, self.y)
                    self.shark_reproduction_counter = 0
                
                self.do_movement = True
                return True
        
        # Réduire l'énergie seulement après avoir vérifié si on peut manger
        self.shark_energy -= 1
        
        # Si pas de sardine à proximité, déplacement normal
        return super().to_moov(ocean)
    
    def check_survival(self, ocean):
        # Si le requin n'a plus d'énergie, il meurt
        if self.shark_energy <= 0:
            ocean.remove_sardine(self.x, self.y)
            return False
        return True