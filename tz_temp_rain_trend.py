import pandas as pd
import matplotlib.pyplot as plt

# --- Data Loading ---
df = pd.read_csv("taiz_daily_climate_1981_2025_full.csv")
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df['Year'] = df['Date'].dt.year

# --- Processing ---
yearly_temp = df.groupby('Year')['Avg_Temp_C'].mean()
yearly_rain = df.groupby('Year')['Precipitation_mm'].sum()

# --- Visualization ---
fig, ax1 = plt.subplots(figsize=(12, 6))
ax2 = ax1.twinx()

ax1.plot(yearly_temp.index, yearly_temp.values, color='#e74c3c', label='Avg Temp (°C)', marker='o')
ax2.bar(yearly_rain.index, yearly_rain.values, color='#3498db', alpha=0.3, label='Total Rain (mm)')

ax1.set_xlabel('Year')
ax1.set_ylabel('Temperature (°C)', color='#e74c3c')
ax2.set_ylabel('Precipitation (mm)', color='#3498db')

plt.title('Interannual Variability: Temperature vs. Precipitation')
plt.tight_layout()
plt.show()