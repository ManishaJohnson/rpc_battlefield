# rpc_battlefield

Group details:
2022H1120281P - Manisha K Johnson
2022H1120286P - Jyotsana Chandrakar

Create a battlefield scenario using remote procedure calls

This project is a simulation of an NxN battlefield with M soldiers and missile attacks. One of the M soldiers is chosen as a Commander, and missiles are launched at random intervals. The system uses Remote Procedure Calls (RPC) for communication between the soldiers and the commander.

## Prerequisites
- Python 3.x
- RPyC library (`pip install rpyc`)

## Setup
1. Clone the repository to your local machine.
   ```
   git clone https://github.com/ManishaJohnson/rpc_battlefield.git
   ```

2. Navigate to the project directory.
   ```
   cd [../rpc_battlefield]
   ```

3. Install the required libraries.
   ```
   pip install -r requirements.txt
   ```

## Running the Simulation

1. Start the RPC server (Commander) on one machine.
   ```
   python commander_server.py
   ```

2. Start the soldier clients on the same machine or other machines.
   ```
   python soldier_client.py
   ```


3. Hyperparameters can be adjusted in the `variables.py` file:
- `N`: Battlefield size (Grid Size)
- `M`: Number of soldiers ()
- `t`: Time interval for missile strikes
- `T`: Total time of simulation
- `Si`: Speed of soldiers (randomly assigned between 0 and 4)

## Output

The program will display:

- The battlefield layout after each missile strike.
- The positions of each soldier (numbered 1, 2, 3, etc.).
- The recent missile landing zone.
- Dead soldiers and the current time (iteration).

Check outputlog.txt for detailed view

---

