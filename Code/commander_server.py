import rpyc
import random
from rpyc.utils.server import ThreadedServer
from soldier import Soldier
from missile import Missile
from variables import Grid_size, Num_soldier, Missile_interval, Deadline, Port_number

N = Grid_size
M = Num_soldier
T = Deadline
t = Missile_interval

# Initialize the battlefield (field matrix)
field = [['.' for _ in range(N)] for _ in range(N)]

class CommanderService(rpyc.Service):
    def exposed_get_battlefield(self, N):
        return self.exposed_Battlefield(N)
            
    class exposed_Battlefield:
        def __init__(self, N):
            self.N = N
            self.soldiers = [Soldier(i+1) for i in range(Num_soldier)]
            self.commander = self.randomly_assign_commander()
            self.field = [['.' for _ in range(N)] for _ in range(N)]
            self.dead_soldiers = set()
            self.live_soldiers = list(range(1, M + 1)) 
        
        def randomly_assign_commander(self):
            commander = random.choice(self.soldiers)
            commander.is_commander = True
            print(f"[SOLDIER {commander.id}] is the commander!")
            return commander

        def exposed_status_all(self):
            return {
                "soldiers": [(s.id, s.is_alive) for s in self.soldiers],
                "commander": (self.commander.id, self.commander.is_alive)
            }

        def exposed_printLayout(self, time):
            output = []
            for i in range(self.N):
                row = []
                for j in range(self.N):
                    if self.field[i][j] == 'R':
                        row.append('R')
                    elif any(s.position == (i, j) and s.is_alive for s in self.soldiers):
                        row.append('S')
                    else:
                        row.append('.')
                output.append(' '.join(row))
            dead_soldiers_count = len([s for s in self.soldiers if not s.is_alive])
            output.append(f"Dead soldiers: {', '.join(map(str, self.dead_soldiers))}, Time: {time}")
            return "\n".join(output)
        
        def exposed_clear_missile_impacts(self):
            for i in range(self.N):
                for j in range(self.N):
                    if self.field[i][j] == 'R':
                        self.field[i][j] = '.'
            dead_soldiers = [soldier.id for soldier in self.soldiers if not soldier.is_alive]
            self.exposed_update_dead_soldiers(dead_soldiers)

        def exposed_missile_approaching(self, position, missile_type):
            print(f"[COMMANDER] Missile of type {missile_type} approaching at position {position}")          
            missile = Missile(missile_type, *position)
            impact_coords = missile.impact_coordinates()
            
            # Update the battlefield based on missile impact
            for x, y in impact_coords:
                if 0 <= x < self.N and 0 <= y < self.N:
                    self.field[x][y] = 'R'

            # Update soldier status
            if self.commander.is_alive:
                for soldier in self.soldiers:
                    if soldier.is_alive:
                        self.take_shelter(soldier.id)
            
            # Now, continue with the original logic of communicating with live soldiers
            for soldier_id in self.live_soldiers:
                soldier = next((s for s in self.soldiers if s.id == soldier_id), None)
                if soldier:
                    soldier.receive_alert(position, missile_type)

            return position, missile_type 

        def exposed_update_dead_soldiers(self, dead_soldiers):
            for dead_soldier in dead_soldiers:
                if dead_soldier in self.live_soldiers:
                    self.live_soldiers.remove(dead_soldier)

        def take_shelter(self, soldier_id):
            print("takeshelter")
            soldier = next((s for s in self.soldiers if s.id == soldier_id), None)  # Use `s.id` not `s.soldierID`
            if soldier and soldier.is_alive:
                if self.field[soldier.position[0]][soldier.position[1]] == 'R':  # Corrected access
                    soldier.is_alive = False
                    self.dead_soldiers.add(soldier.id)  # This line needs the dead_soldiers list to be defined somewhere in the class
                else:
                    soldier.move_randomly(self.N)

        def exposed_was_hit(self, soldierID, trueFlag):
            soldier = next((s for s in self.soldiers if s.id == soldierID), None)
            if soldier:
                soldier.is_alive = not trueFlag
                if trueFlag:
                    self.dead_soldiers.add(soldierID)  
                    self.field[soldier.position[0]][soldier.position[1]] = '.'

        def exposed_battle_outcome(self):
            alive_count = sum(1 for s in self.soldiers if s.is_alive)
            if alive_count > Num_soldier / 2:
                return "Battle is won."
            else:
                return "Battle is lost."
        
        def exposed_update_commander(self, new_commander_id):
            self.commander = next((s for s in self.soldiers if s.id == new_commander_id), None)
            self.commander.is_commander = True

if __name__ == "__main__":
    t = ThreadedServer(CommanderService, port=Port_number)    
    t.start()