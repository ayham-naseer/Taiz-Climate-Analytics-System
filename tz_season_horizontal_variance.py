import pandas as pd
import matplotlib.pyplot as plt

# --- 1. Configuration ---
FILE_PATH = "taiz_daily_climate_1981_2025_full.csv"
COLORS = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12']
ORDER = ['Winter', 'Spring', 'Summer', 'Autumn']

def prepare_horizontal_data():
    """Processes data specifically for horizontal variance mapping."""
    with open(FILE_PATH, 'r', encoding='utf-8') as file:
        df = pd.read_csv(file)
        
    df['Date'] = pd.to_datetime(df['Date'])
    df['Year'] = df['Date'].dt.year
    df['Temp_Smooth'] = df['Avg_Temp_C'].rolling(window=14, center=True).mean()

    def classify(row):
        t, m = row['Temp_Smooth'], row['Date'].month
        if pd.isna(t): return 'Unknown'
        if t >= 23.5: return 'Summer'
        elif t <= 20.5: return 'Winter'
        else: return 'Spring' if 2 <= m <= 6 else 'Autumn'

    df['Season'] = df.apply(classify, axis=1)
    counts = df.groupby(['Year', 'Season']).size().unstack(fill_value=0).reindex(columns=ORDER, fill_value=0)
    return counts.div(counts.sum(axis=1), axis=0) * 100

def plot_horizontal_map(percentages):
    """Renders a horizontal stacked bar chart."""
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(12, 14)) 

    percentages.plot(kind='barh', stacked=True, color=COLORS, width=0.8, ax=ax)

    # Embed percentage labels
    for container in ax.containers:
        labels = [f'{w:.1f}%' if w > 5 else '' for w in container.datavalues]
        ax.bar_label(container, labels=labels, label_type='center', fontsize=8, color='white', fontweight='bold')

    ax.set_title('Horizontal Analysis of Seasonal Variance in Taiz (1981-2025)\nNote: Annual fluctuations reflect natural oscillation around thermal thresholds', 
                 fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('Percentage of Days per Year (%)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Year', fontsize=12, fontweight='bold')
    ax.legend(title='Season', bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    pct_data = prepare_horizontal_data()
    plot_horizontal_map(pct_data)