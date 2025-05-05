from models.fishes import Fish

class Shark(Fish):
    def __init__(self, x=0, y=0, age=0, shark_energy=3, shark_starvation_time=1, shark_reproduction_time=3):
        super().__init__(x, y, age)
        self.shark_energy = shark_energy
        self.shark_starvation_time = shark_starvation_time
        self.shark_reproduction_time = shark_reproduction_time
    
    def move_shark(self, ocean):
        self.age += 1
        self.shark_energy -= 1
        self.shark_reproduction_time += 1
        
        # Vérifie s'il y a des sardines à proximité pour manger
        neighbor_fish = ocean.fish_neighbour(self.x, self.y)
        
        if neighbor_fish:
            # Manger une sardine et gagner de l'énergie
            fish_x, fish_y = ocean.random_choice(neighbor_fish)
            ocean.eat_fish(self.x, self.y, fish_x, fish_y)
            self.x, self.y = fish_x, fish_y
            self.shark_energy += 2  # Gain d'énergie en mangeant
            
            # Vérifier si reproduction possible
            if self.shark_reproduction_time >= self.shark_reproduction_time:
                ocean.add_fish(self.x, self.y, Shark)
                self.shark_reproduction_time = 0
                
            return True
        
        # Si pas de sardine à proximité, déplacement normal
        return super().to_move(ocean)
    
    def check_survival(self, ocean):
        # Si le requin n'a plus d'énergie, il meurt
        if self.shark_energy <= 0:
            ocean.remove_fish(self.x, self.y)
            return False
        return True