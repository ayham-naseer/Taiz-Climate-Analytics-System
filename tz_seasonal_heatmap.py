import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("taiz_daily_climate_1981_2025_full.csv")
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

# Matrix transformation for heatmap
heatmap_data = df.groupby([df['Date'].dt.year, df['Date'].dt.month])['Avg_Temp_C'].mean().unstack()

plt.figure(figsize=(14, 10))
sns.heatmap(heatmap_data, cmap='coolwarm')
plt.title('Monthly Temperature Intensity')
plt.gca().invert_yaxis() 
plt.show()