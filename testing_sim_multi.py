import subprocess
import csv
import re
import numpy as np
import os
import sys

# Parameters to test
parameters = ['Water_Bodies'] #['LCohesion', 'LSeparation', 'LDefend', 'LPerception']
values = {
    'LCohesion': [0.0, 2.0], 
    'LSeparation': [0.0, 3.0], 
    'LDefend': [0.0, 6.0], 
    'LPerception': [0, 300],
    'Lnum': [1, 5],
    'Lpred': [1, 5],
    'Water_Bodies': [0,3],
}
runs_per_param = {
    'LCohesion': 3,
    'LSeparation': 4,
    'LDefend': 7,
    'LPerception': 5,
    'Lnum': 6,
    'Water_Bodies': 4,
}
time = '60' # Run the simulation for 60 seconds

simulation_script = "Simulation.py"
output_csv = "results_water.csv"

# Regular expression to extract "Sheep Left" value
sheep_regex = re.compile(r"Sheep Left: (\d+)")

# Get path
script_path = os.path.abspath(simulation_script)

with open(output_csv, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow([f"Parameter", "Value", "Num llamas", "Num Preds", "Run", "SheepLeft"])

    for parameter in parameters:
      test_values = np.linspace(values[parameter][0], values[parameter][1], runs_per_param[parameter])
      pred_values = np.linspace(values['Lpred'][0], values['Lpred'][1], 5)
      num_values = np.linspace(values['Lnum'][0], values['Lnum'][1], 5)
      num_runs = 5

      for val in test_values:
        for pred in pred_values:
          for num in num_values:
            for run in range(1, num_runs + 1):
                print(f"Running {parameter}={val}, Llamas={num}, Predators={pred}, Run {run}...")

                result = subprocess.run(
                    [
                        "python", script_path, 
                        f"--{parameter.lower()}", str(int(val)),
                        "--time", time,
                        "--lpred", str(int(pred)),
                        "--lnum", str(int(num))
                    ],
                    capture_output=True,
                    text=True,
                    shell=False,
                )

                if (result.stderr):
                    print(result.stderr)

                # Extract "Sheep Left" from stdout
                match = sheep_regex.search(result.stdout)
                if match:
                    sheep_left = int(match.group(1))
                    writer.writerow([parameter, val, num, pred, run, sheep_left])
                else:
                    print("Could not extract Sheep Left from output!")
