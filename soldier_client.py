import rpyc
import random
import time
from missile import Missile
from soldier import Soldier
from variables import Grid_size, Num_soldier, Missile_interval, Deadline, Port_number
N = Grid_size  # Battlefield size
M = Num_soldier
T = Deadline  # Total time of simulation
t = Missile_interval   # Time interval for missile strikes

def connect_to_battlefield():
    conn = rpyc.connect("localhost", 18861)
    battlefield = conn.root.get_battlefield(N)
    return battlefield

def randomly_assign_commander(soldiers):
    commander = random.choice(soldiers)
    commander.is_commander = True
    print(f"[SOLDIER {commander.id}] is the commander!")
    return commander

def simulate():
    soldiers = [Soldier(i+1) for i in range(M)]
    commander = randomly_assign_commander(soldiers)
    missile_launcher = Missile(0, 0, 0)  # Dummy instance for launching missiles
    battlefield = connect_to_battlefield()
    print(battlefield.printLayout(t))

    for i in range(0, T, t):
        print(f"Time Interval: {i} ----------------------------------------------------------")
        
        #Missile Launch
        time.sleep(2)  # Delay for missile impact
        x, y = random.randint(0, N - 1), random.randint(0, N - 1)
        missile_position = (random.randint(0, N-1), random.randint(0, N-1))
        missile_type = missile_launcher.missile_launch(x, y)

        #Broadcast to all soldiers if alive
        for soldier in soldiers:
            if soldier.is_alive:
                try:
                    alert_position, alert_type = battlefield.missile_approaching(missile_position, missile_type)
                    soldier.receive_alert(alert_position, alert_type)
                except ConnectionRefusedError:
                    print("Commander (Server) not available!")

        #check impact
        for soldier in soldiers:
            soldier.check_impact(missile_position, missile_type)
            if not soldier.is_alive:
                battlefield.was_hit(soldier.id, True)

        print(battlefield.printLayout(i))
        
        status = battlefield.status_all()
        print("Status:", status)
        commander_status = status["commander"][1]

        if not commander_status:
            print(f"[COMMANDER]Commander is dead in battle Interval {i}")

        dead_count = sum(1 for _, alive in status["soldiers"] if not alive)
        if dead_count > M / 2:
            print("Battle is lost.")
            return
        if not commander_status:
            alive_soldiers_ids = [s_id for s_id, alive in status["soldiers"] if alive]
            new_commander_id = random.choice(alive_soldiers_ids)
            commander = next(s for s in soldiers if s.id == new_commander_id)
            print(f"[SOLDIER {commander.id}] is the new commander!")
            battlefield.update_commander(commander.id)  # Update the commander on the server
        
        # Clear missile impact for the next round
        battlefield.clear_missile_impacts()
        print(f"---------------------------------------------------------------------------")
        print()
        time.sleep(2) 
    print(battlefield.battle_outcome())

if __name__ == "__main__":
    simulate()