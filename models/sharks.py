from utils.config import *
from models.fishes import *
from ocean.ocean import *

class Shark(Fish):
    def __init__(self, shark_energy, shark_starvation_time, shark_reproduction_time):
        super().__init__()  # si Poisson a des attributs à initier
        self.shark_energy = shark_energy
        self.shark_starvation_time = shark_starvation_time
        self.shark_reproduction_time = shark_reproduction_time
        self.age = 0  # utile pour reproduction


def move_shark(self, position, ocean):
    self.age += 1
    self.shark_energy -= 1
    self.shark_reproduction_time += 1

 def shark_reproduction(shark, grid, reproduction_threshold):
    """
    Handles the reproduction of a shark in the simulation.

    Parameters:
        shark (dict): A dictionary representing the shark, containing its position and reproduction counter.
                      Example: {'x': 2, 'y': 3, 'reproduction_counter': 3}
        grid (list of list): The simulation grid where sharks and fish live.
        reproduction_threshold (int): The threshold at which the shark reproduces.

    Returns:
        dict or None: A new shark dictionary if reproduction occurs, otherwise None.
    """
    # Decrease the reproduction counter
    shark['reproduction_counter'] -= 1

    # Check if the shark is ready to reproduce
    if shark['reproduction_counter'] <= 0:
        # Reset the reproduction counter
        shark['reproduction_counter'] = reproduction_threshold

        # Find an empty adjacent cell for the new shark
        x, y = shark['x'], shark['y']
        empty_cells = []

        # Check adjacent cells (up, down, left, right)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] is None:
                empty_cells.append((nx, ny))

        if empty_cells:
            # Choose a random empty cell for the new shark
            import random
            new_x, new_y = random.choice(empty_cells)

            # Place the new shark on the grid
            new_shark = {'x': new_x, 'y': new_y, 'reproduction_counter': reproduction_threshold}
            grid[new_x][new_y] = new_shark

            return new_shark

    return None

def shark_starvation_time(shark, grid, starvation_threshold):
    """
    Handles the starvation logic for a shark in the simulation.

    Parameters:
        shark (dict): A dictionary representing the shark, containing its position and starvation counter.
                      Example: {'x': 2, 'y': 3, 'starvation_counter': 3}
        grid (list of list): The simulation grid where sharks and fish live.
        starvation_threshold (int): The threshold at which the shark dies from starvation.

    Returns:
        bool: True if the shark survives, False if it dies from starvation.
    """
    # Decrease the starvation counter
    shark['starvation_counter'] -= 1

    # Check if the shark has starved
    if shark['starvation_counter'] <= 0:
        # Remove the shark from the grid
        x, y = shark['x'], shark['y']
        grid[x][y] = None
        return False  # Shark has died

    return True  # Shark survives

def move_shark(shark, grid):
    """
    Moves a shark to an adjacent cell in the simulation grid.

    Parameters:
        shark (dict): A dictionary representing the shark, containing its position.
                      Example: {'x': 2, 'y': 3, 'reproduction_counter': 3, 'starvation_counter': 5}
        grid (list of list): The simulation grid where sharks and fish live.

    Returns:
        bool: True if the shark moved, False if it stayed in place.
    """
    x, y = shark['x'], shark['y']
    possible_moves = []

    # Check adjacent cells (up, down, left, right)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]):
            if grid[nx][ny] is None or isinstance(grid[nx][ny], dict) and grid[nx][ny].get('type') == 'fish':
                possible_moves.append((nx, ny))

    if possible_moves:
        # Choose a random valid move
        import random
        new_x, new_y = random.choice(possible_moves)

        # Update the grid
        grid[x][y] = None  # Remove shark from current position
        grid[new_x][new_y] = shark  # Place shark in the new position

        # Update shark's position
        shark['x'], shark['y'] = new_x, new_y

        return True  # Shark moved

    return False  # Shark stayed in place

def shark_energy(shark, grid, energy_gain, energy_loss):
    """
    Updates the energy level of a shark based on its actions in the simulation.

    Parameters:
        shark (dict): A dictionary representing the shark, containing its position and energy level.
                      Example: {'x': 2, 'y': 3, 'energy': 5}
        grid (list of list): The simulation grid where sharks and fish live.
        energy_gain (int): The amount of energy the shark gains when eating a fish.
        energy_loss (int): The amount of energy the shark loses per turn.

    Returns:
        bool: True if the shark survives, False if it dies due to lack of energy.
    """
    x, y = shark['x'], shark['y']

    # Check if the shark eats a fish
    if isinstance(grid[x][y], dict) and grid[x][y].get('type') == 'fish':
        # Gain energy from eating the fish
        shark['energy'] += energy_gain
        grid[x][y] = None  # Remove the fish from the grid
    else:
        # Lose energy if no fish is eaten
        shark['energy'] -= energy_loss

    # Check if the shark runs out of energy
    if shark['energy'] <= 0:
        # Remove the shark from the grid
        grid[x][y] = None
        return False  # Shark has died

    return True  # Shark survives