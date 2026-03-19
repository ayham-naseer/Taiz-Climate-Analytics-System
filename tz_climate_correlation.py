import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# --- Data Loading ---
df = pd.read_csv("taiz_daily_climate_1981_2025_full.csv")
df['DTR'] = df['Max_Temp_C'] - df['Min_Temp_C'] # Engineering Diurnal Temp Range

# --- Statistical Analysis ---
# Using Spearman to capture non-linear climate relationships
features = ['Avg_Temp_C', 'Precipitation_mm', 'Relative_Humidity_Percent', 'Wind_Speed_m_s', 'DTR']
corr_matrix = df[features].corr(method='spearman')

# --- Visualization ---
plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap='RdYlGn', center=0, fmt=".2f")
plt.title('Spearman Correlation: Climate Variables Interaction')
plt.tight_layout()
plt.show()