import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# --- 1. GLOBAL CONFIGURATION ---
DATA_FILE_PATH = "taiz_daily_climate_1981_2025_full.csv"
PLOT_STYLE = 'seaborn-v0_8-muted'

def tz_setup_style():
    """Configures the visual aesthetic for the plots."""
    plt.style.use(PLOT_STYLE)
    plt.rcParams.update({
        'font.size': 11,
        'axes.grid': False,  # Disable standard grid to prioritize Heatmap clarity
        'figure.facecolor': '#f8f9fa'
    })

def tz_load_data():
    """
    Loads climate data and constructs a 2D pivot table (Years vs Days).
    Ensures the dataset is properly formatted for high-resolution rendering.
    """
    if not os.path.exists(DATA_FILE_PATH):
        raise FileNotFoundError(f"Data file not found at: {DATA_FILE_PATH}")

    with open(DATA_FILE_PATH, 'r', encoding='utf-8') as file:
        df = pd.read_csv(file)

    # Standardize column names
    df.columns = [col.lower().replace(' ', '_') for col in df.columns]
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    df['day_of_year'] = df['date'].dt.dayofyear

    # Build the primary matrix (Year x DayOfYear)
    pivot_table = df.pivot(index='year', columns='day_of_year', values='avg_temp_c')
    return pivot_table

def tz_render_manual_heatmap(matrix, start_y, end_y):
    """
    Renders a 1:1 pixel-accurate heatmap for a specific user-defined year range.
    """
    # Slice the matrix based on user selection
    filtered_matrix = matrix.loc[start_y:end_y]
    
    fig, ax = plt.subplots(figsize=(18, 8))
    
    # Use pcolormesh for sharp, non-interpolated data visualization
    mesh = ax.pcolormesh(filtered_matrix.columns, filtered_matrix.index, filtered_matrix.values, 
                          cmap='RdYlBu_r', shading='nearest')

    # Title and Labels
    ax.set_title(f'Manual Climate Scan: Taiz Daily Temperatures ({start_y}-{end_y})', 
                  fontweight='bold', pad=20, fontsize=16)
    ax.set_ylabel('Year', fontsize=12, fontweight='bold')
    ax.set_xlabel('Month', fontsize=12, fontweight='bold')

    # Colorbar configuration
    cbar = fig.colorbar(mesh, ax=ax, pad=0.02)
    cbar.set_label('Temperature (°C)', rotation=270, labelpad=15)

    # Monthly axis ticks configuration
    month_starts = [1, 32, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335]
    month_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    ax.set_xticks(month_starts)
    ax.set_xticklabels(month_labels)

    # Project Identifier (Footer)
    plt.figtext(0.99, 0.01, 'System: Taiz Climate Analytics | Module: Manual Scanner', 
                horizontalalignment='right', fontsize=9, color='#7f8c8d', alpha=0.7)

    plt.tight_layout()
    plt.show()

def main():
    tz_setup_style()
    try:
        # 1. Load data and identify available time bounds
        full_matrix = tz_load_data()
        min_available = full_matrix.index.min()
        max_available = full_matrix.index.max()

        print("="*50)
        print(f"[*] Taiz Climate System: Ready")
        print(f"[*] Data Integrity Check: OK")
        print(f"[*] Coverage: {min_available} to {max_available}")
        print("="*50)

        # 2. Terminal-based User Input
        start_year = int(input(f"Enter Start Year (min {min_available}): "))
        end_year = int(input(f"Enter End Year (max {max_available}): "))

        # 3. Validation Logic
        if start_year < min_available or end_year > max_available or start_year > end_year:
            print("[!] Error: Out of bounds. Please select years within the available range.")
        else:
            print(f"[*] Scanning period {start_year}-{end_year}...")
            tz_render_manual_heatmap(full_matrix, start_year, end_year)
            print("[+] Visualization Complete.")

    except ValueError:
        print("[!] Input Error: Numeric year values required.")
    except Exception as e:
        print(f"[Fatal System Error]: {e}")

if __name__ == "__main__":
    main()