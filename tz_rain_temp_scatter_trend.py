import pandas as pd
import matplotlib.pyplot as plt

# --- 1. Data Setup ---
FILE_PATH = "taiz_daily_climate_1981_2025_full.csv"
df = pd.read_csv(FILE_PATH)
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df['Year'] = df['Date'].dt.year

# Annual Aggregation
annual_df = df.groupby('Year').agg({
    'Avg_Temp_C': 'mean',
    'Precipitation_mm': 'sum'
}).reset_index()

# --- 2. Rolling Correlation Calculation ---
# Window of 10 years to smooth out short-term noise and show decadal shifts
WINDOW_SIZE = 10
annual_df['Rolling_r'] = annual_df['Avg_Temp_C'].rolling(window=WINDOW_SIZE).corr(annual_df['Precipitation_mm'])

# --- 3. Visualization ---
plt.figure(figsize=(12, 6))
plt.plot(annual_df['Year'], annual_df['Rolling_r'], color='#2980b9', linewidth=2.5, marker='s', markersize=4)

# Visualizing the "Zero Line" (No Correlation)
plt.axhline(0, color='black', linestyle='--', alpha=0.3)

plt.title(f'{WINDOW_SIZE}-Year Rolling Correlation: Rain vs. Temp', fontsize=14)
plt.xlabel('Year (End of Window)')
plt.ylabel('Correlation Coefficient (r)')
plt.grid(True, linestyle=':', alpha=0.6)

plt.tight_layout()
plt.show()