import random

class Missile:
    def __init__(self, missile_type, x, y):
        self.missile_type = missile_type
        self.x = x
        self.y = y
        self.missiles = []

    def impact_coordinates(self):
        coords = []
        if self.missile_type == 1:
            coords.append((self.x, self.y))
        elif self.missile_type == 2:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    coords.append((self.x + dx, self.y + dy))
        elif self.missile_type == 3:
            for dx in [-2, -1, 0, 1, 2]:
                for dy in [-2, -1, 0, 1, 2]:
                    coords.append((self.x + dx, self.y + dy))
        elif self.missile_type == 4:
            for dx in [-3, -2, -1, 0, 1, 2, 3]:
                for dy in [-3, -2, -1, 0, 1, 2, 3]:
                    coords.append((self.x + dx, self.y + dy))
        return coords
    
    def missile_launch(self, x, y):
        missile_type = random.randint(1, 4)
        missile_name = f"M{missile_type}"
        self.missiles.append(Missile(missile_type, x, y))
        print(f"Missile {missile_name} launched targeting ({x}, {y})")
        return missile_type