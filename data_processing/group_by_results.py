import pandas as pd

# Read your original spreadsheet
df = pd.read_csv('./../results_water.csv')  # Replace with your file name

# Group by the columns you want and take the mean of "Num Sheep Alive"
grouped = df.groupby(['Parameter', 'Value', 'Num llamas', 'Num Preds'])['SheepLeft'].mean().reset_index()

# Rename the averaged column if you want
grouped = grouped.rename(columns={'Num Sheep Alive': 'Average Sheep Alive'})

# Save to a new CSV
grouped.to_csv('averaged_results_w.csv', index=False)
