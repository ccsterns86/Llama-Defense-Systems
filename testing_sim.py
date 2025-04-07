import subprocess
import csv
import re
import numpy as np
import os

# Parameters to test
parameters = [ 'Perception' ]#['Cohesion', 'Separation', 'Defend', 'Perception']
values = {
    'Cohesion': [0.0, 2.0], 
    'Separation': [0.0, 3.0], 
    'Defend': [0.0, 6.0], 
    'Perception': [0, 300]
}
runs_per_param = {
    'Cohesion': 5, 
    'Separation': 5, 
    'Defend': 6, 
    'Perception': 10
}
time = '60' # Run the simulation for 60 seconds

simulation_script = "Simulation.py"  # replace with your actual script
output_csv = "perception_results.csv"

# Regular expression to extract "Sheep Left" value
sheep_regex = re.compile(r"Sheep Left: (\d+)")

# Get path
script_path = os.path.abspath(simulation_script)

with open(output_csv, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow([f"Parameter", "Value", "Run", "SheepLeft"])

    for parameter in parameters:
      test_values = np.linspace(values[parameter][0], values[parameter][1], runs_per_param[parameter])
      num_runs = 5

      for val in test_values:
          for run in range(1, num_runs + 1):
              print(f"Running {parameter}={val}, run {run}...")

              result = subprocess.run(
                  ["python", script_path, f"--l{parameter.lower()}", str(val), "--time", f"{time}"],
                  capture_output=True,
                  text=True,
                  shell=False
              )

              if (result.stderr):
                  print(result.stderr)
                  print("Terminating!")
                  exit()

              # Extract "Sheep Left" from stdout
              match = sheep_regex.search(result.stdout)
              print(result.stdout) # TODO: remove
              if match:
                  sheep_left = int(match.group(1))
                  writer.writerow([parameter, val, run, sheep_left])
              else:
                  print("Could not extract Sheep Left from output!")

              #input("Press Enter to continue...")
