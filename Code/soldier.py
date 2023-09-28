import random
from variables import Grid_size, Num_soldier, Missile_interval, Deadline, Port_number, Soldier_speed
N = Grid_size  # Battlefield size
M = Num_soldier
T = Deadline  # Total time of simulation
t = Missile_interval   # Time interval for missile strikes
Si = Soldier_speed
class Soldier:
    def __init__(self, soldier_id):
        self.id = soldier_id
        self.position = (random.randint(0, N-1), random.randint(0, N-1))
        self.speed = random.randint(0, Si)
        self.is_alive = True
        self.is_commander = False

    def receive_alert(self, position, missile_type):
        if self.position == position and self.is_alive:
            print(f"[SOLDIER {self.id}] In danger! Current position: {self.position}")
            self.position = (self.position[0], min(self.position[1] + 1, N-1))
            print(f"[SOLDIER {self.id}] Moved to {self.position}")

    def check_impact(self, position, missile_type):
        if self.position == position:
            self.is_alive = False
            print(f"[SOLDIER {self.id}] Hit by missile and is now dead.")

    def move_randomly(self, N):
        for _ in range(self.speed):
            dx, dy = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)])
            new_x, new_y = self.position[0] + dx, self.position[1] + dy
            if 0 <= new_x < N and 0 <= new_y < N:
                self.position = (new_x, new_y)