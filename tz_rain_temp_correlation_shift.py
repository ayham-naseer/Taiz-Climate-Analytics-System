import pandas as pd

# --- 1. Data Loading & Chronological Setup ---
FILE_PATH = "taiz_daily_climate_1981_2025_full.csv"
df = pd.read_csv(FILE_PATH)

df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df['Year'] = df['Date'].dt.year

# --- 2. Feature Aggregation ---
# Aggregating to annual level to filter daily noise and capture long-term climate signals
annual_df = df.groupby('Year').agg({
    'Avg_Temp_C': 'mean',
    'Precipitation_mm': 'sum'
}).reset_index()

# --- 3. Decadal Correlation Analysis ---
# Segmenting the data into two distinct eras for comparative analysis

# Historical Period: The 1980s (Baseline)
eighties = annual_df[(annual_df['Year'] >= 1981) & (annual_df['Year'] <= 1990)]
corr_80s = eighties['Avg_Temp_C'].corr(eighties['Precipitation_mm'])

# Recent Period: The last decade (Current Trend)
recent = annual_df[(annual_df['Year'] >= 2015) & (annual_df['Year'] <= 2025)]
corr_recent = recent['Avg_Temp_C'].corr(recent['Precipitation_mm'])

# --- 4. Output Results ---
print(f"Rain-Temperature Correlation (1981-1990): {corr_80s:.2f}")
print(f"Rain-Temperature Correlation (2015-2025): {corr_recent:.2f}")