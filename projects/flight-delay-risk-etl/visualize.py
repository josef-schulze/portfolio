import duckdb
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
import logging
from zoneinfo import ZoneInfo
from config import DB_FILE, TABLE_NAME, IMAGE_OUTPUT, AIRPORT_INFO, TZ

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_recent_data():
    conn = duckdb.connect(DB_FILE)
    query = f"SELECT * FROM {TABLE_NAME} ORDER BY observation_time"
    df = conn.execute(query).df()
    conn.close()
    return df

def generate_dashboard():
    logging.info("Generating dashboard...")
    df = load_recent_data()
    
    if df.empty:
        logging.warning("No data available")
        return
    
    # Timezone handling
    df['observation_time'] = pd.to_datetime(df['observation_time'])
    df['observation_time'] = df['observation_time'].dt.tz_localize('UTC').dt.tz_convert(TZ)
    plot_times = df['observation_time'].copy()
    df['observation_time'] = plot_times.dt.tz_localize(None)
    
    print("✅ First plotted timestamp:", plot_times.iloc[0])
    
    sns.set_theme(style="whitegrid")
    fig = plt.figure(figsize=(14, 12))
    
    # Consistent colors
    color_dict = {code: color for code, color in zip(AIRPORT_INFO.keys(), sns.color_palette("tab10", len(AIRPORT_INFO)))}
    
    # Top: Line Chart
    ax1 = plt.subplot(2, 1, 1)
    for code, info in AIRPORT_INFO.items():
        airport_data = df[df['airport_code'] == code].copy()
        if airport_data.empty:
            continue
        label = f"{code} - {info['name']}"
        temp_data = airport_data.copy()
        temp_data['observation_time'] = plot_times[airport_data.index]
        sns.lineplot(data=temp_data, x='observation_time', y='risk_score',
                    ax=ax1, marker='o', linewidth=2.5, label=label, color=color_dict[code])
    
    ax1.set_title("Flight Delay Risk Score - All Airports", fontsize=16)
    ax1.set_ylabel("Risk Score (0-100)")
    ax1.set_xlabel("Observation Time (Central Time)")
    ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9)
    ax1.set_ylim(0, 100)
    ax1.grid(True)
    ax1.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%I:%M %p', tz=TZ))
    
    # Bottom: Fixed order bar chart with rich labels
    ax2 = plt.subplot(2, 1, 2)
    
    # Use fixed order from AIRPORT_INFO (matches legend)
    latest = pd.DataFrame({'airport_code': list(AIRPORT_INFO.keys())})
    latest = latest.merge(df.groupby('airport_code').last().reset_index(), on='airport_code', how='left')
    
    # Calculate changes
    changes = []
    for code in latest['airport_code']:
        hist = df[df['airport_code'] == code].sort_values('observation_time')
        change = hist['risk_score'].iloc[-1] - hist['risk_score'].iloc[-2] if len(hist) >= 2 else 0
        changes.append(change)
    latest['change'] = changes
    
    # Rich multi-line label
    def make_label(row):
        temp_f = round(row['temperature_c'] * 9/5 + 32) if pd.notna(row['temperature_c']) else '?'
        wind = round(row['wind_mph']) if pd.notna(row['wind_mph']) else '?'
        vis = round(row['visibility_miles'], 1) if pd.notna(row['visibility_miles']) else '?'
        weather = str(row['text_description'])[:28] if pd.notna(row['text_description']) else 'Unknown'
        
        base = f"{row['airport_code']} - {AIRPORT_INFO.get(row['airport_code'], {}).get('name', '')}"
        return f"{base}\n{temp_f}°F | {wind} mph winds\nVisibility {vis} miles\n{weather}"
    
    latest['display_label'] = latest.apply(make_label, axis=1)
    
    bar_colors = [color_dict[code] for code in latest['airport_code']]
    
    sns.barplot(
        data=latest,
        x='display_label',
        y='risk_score',
        ax=ax2,
        palette=bar_colors,
        hue='display_label',
        legend=False
    )
    
    ax2.set_title("Current Risk Levels + Conditions", fontsize=14)
    ax2.set_ylabel("Risk Score (0-100)")
    ax2.set_xlabel("")
    ax2.set_ylim(0, 100)
    plt.xticks(rotation=45, ha='right')
    
    # Value labels with change arrows
    for i, p in enumerate(ax2.patches):
        height = p.get_height() if not pd.isna(p.get_height()) else 0
        change = latest.iloc[i]['change']
        arrow = "↑" if change > 0 else "↓" if change < 0 else "→"
        ax2.annotate(f"{int(height)} {arrow}{abs(change)}", 
                    (p.get_x() + p.get_width()/2., height + 1.5),
                    ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    note_text = ("Note: Arrows indicate change from previous run\n"
                 "↑ = increased risk    ↓ = decreased risk    → = no change")
    fig.text(0.5, 0.02, note_text, ha='center', fontsize=10, 
             bbox=dict(boxstyle="round", facecolor="lightgray", alpha=0.8))
    
    plt.suptitle(f"Real-Time Flight Delay Risk Tracker - Central Time\n"
                 f"Updated: {datetime.now(TZ).strftime('%Y-%m-%d %I:%M %p %Z')}", 
                 fontsize=18, y=0.96)
    
    plt.tight_layout(rect=[0, 0.05, 1, 0.95])
    plt.savefig(IMAGE_OUTPUT, dpi=300, bbox_inches='tight')
    plt.close()
    
    logging.info(f"✅ Dashboard saved as {IMAGE_OUTPUT}")

if __name__ == "__main__":
    generate_dashboard()