import pandas as pd
import matplotlib.pyplot as plt

# Load and prepare dataset
df = pd.read_csv("taiz_daily_climate_1981_2025_full.csv")
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

# Calculate annual average
yearly_data = df.groupby(df['Date'].dt.year)['Avg_Temp_C'].mean()

# Visualization
plt.figure(figsize=(12, 5))
plt.plot(yearly_data.index, yearly_data.values, marker='o', color='#c0392b')
plt.title('Annual Average Temperature (1981 - 2025)')
plt.xlabel('Year')
plt.ylabel('Temp (°C)')
plt.grid(True, linestyle='--')
plt.tight_layout()
plt.show()