class Fish:
    def __init__(self, x=0, y=0, age=0):
        self.x = x
        self.y = y
        self.age = age
        self.fish_reproduction_time = 0
        self.do_movement = False
    
    def age_up(self):
        self.age += 1
        self.fish_reproduction_time += 1
    
    def can_reproduced(self):
        from models.utils.config import FISH_REPRODUCTION_TIME
        return self.fish_reproduction_time >= FISH_REPRODUCTION_TIME
    
    def to_reproduced(self):
        self.fish_reproduction_time = 0
    
    def to_moov(self, ocean):
        if self.do_movement:
            return False
        
        neighbour_empty = ocean.empty_box_neighbour(self.x, self.y)
        
        if not neighbour_empty:
            return False
        
        new_x, new_y = ocean.random_choice(neighbour_empty)
        if new_x is None or new_y is None:
            return False
        
        have_to_reproduced = self.can_reproduced()
        
        ocean.moov_sardine(self.x, self.y, new_x, new_y)
        self.x, self.y = new_x, new_y
        
        if have_to_reproduced:
            self.to_reproduced()
            ocean.add_sardine(self.x, self.y)
            
        self.do_movement = True
        return True