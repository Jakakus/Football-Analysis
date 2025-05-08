import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from arsenal_striker_analysis import combine_player_stats, calculate_striker_suitability

# Set the style for all plots
plt.style.use('default')
sns.set_theme()

def create_radar_chart(player_data, title):
    """Create a radar chart for player performance metrics"""
    categories = ['Goals per 90', 'Conversion Rate', 'Shot Volume', 'Shot Quality', 'Minutes Played']
    
    # Normalize the values for radar chart
    goals_per_90 = player_data['Goals_per_90'] / player_data['Goals_per_90'].max()
    conversion = (player_data['Gls'] / player_data['Sh']) / (player_data['Gls'] / player_data['Sh']).max()
    shot_volume = player_data['Shots_per_90'] / player_data['Shots_per_90'].max()
    shot_quality = (player_data['xG'] / player_data['Sh']) / (player_data['xG'] / player_data['Sh']).max()
    minutes = player_data['90s'] / player_data['90s'].max()
    
    values = [goals_per_90, conversion, shot_volume, shot_quality, minutes]
    
    # Number of variables
    N = len(categories)
    
    # Compute angle for each axis
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]
    
    # Plot
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
    
    # Draw one axis per variable and add labels
    plt.xticks(angles[:-1], categories)
    
    # Draw ylabels (0, 0.2, 0.4, 0.6, 0.8, 1.0)
    ax.set_rlabel_position(0)
    plt.yticks([0.2, 0.4, 0.6, 0.8, 1.0], ["0.2", "0.4", "0.6", "0.8", "1.0"], color="grey", size=8)
    plt.ylim(0, 1)
    
    # Plot data
    values += values[:1]
    ax.plot(angles, values, linewidth=2, linestyle='solid')
    ax.fill(angles, values, alpha=0.4)
    
    plt.title(title, size=15, y=1.1)
    return fig

def create_goals_vs_xg_scatter(df):
    """Create a scatter plot of goals vs expected goals"""
    plt.figure(figsize=(12, 8))
    
    # Create scatter plot
    scatter = plt.scatter(df['xG'], df['Gls'], 
                         c=df['Goals_per_90'], 
                         s=df['90s']*10,
                         cmap='viridis',
                         alpha=0.6)
    
    # Add diagonal line
    max_val = max(df['xG'].max(), df['Gls'].max())
    plt.plot([0, max_val], [0, max_val], '--', color='gray', alpha=0.5)
    
    # Add labels and title
    plt.xlabel('Expected Goals (xG)', fontsize=12)
    plt.ylabel('Actual Goals', fontsize=12)
    plt.title('Goals vs Expected Goals Analysis', fontsize=14)
    
    # Add colorbar
    cbar = plt.colorbar(scatter)
    cbar.set_label('Goals per 90 minutes', fontsize=10)
    
    # Add annotations for top 5 players
    top_players = df.nlargest(5, 'Suitability_Score')
    for _, player in top_players.iterrows():
        plt.annotate(player['Player'], 
                    (player['xG'], player['Gls']),
                    xytext=(5, 5), textcoords='offset points',
                    fontsize=8)
    
    return plt.gcf()

def create_shot_quality_heatmap(df):
    """Create a heatmap of shot quality metrics"""
    metrics = ['Goals_per_90', 'Shots_per_90', 'SoT%', 'Gls', 'xG']
    correlation = df[metrics].corr()
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation, 
                annot=True, 
                cmap='RdBu_r', 
                center=0,
                fmt='.2f',
                square=True)
    
    plt.title('Correlation Matrix of Shot Quality Metrics', fontsize=14)
    return plt.gcf()

def create_performance_comparison(df):
    """Create a comparison of key performance metrics"""
    metrics = ['Goals_per_90', 'Shots_per_90', 'SoT%', 'xG']
    df_melted = pd.melt(df, 
                        id_vars=['Player'], 
                        value_vars=metrics,
                        var_name='Metric', 
                        value_name='Value')
    
    plt.figure(figsize=(12, 6))
    sns.barplot(data=df_melted, x='Player', y='Value', hue='Metric')
    plt.xticks(rotation=45, ha='right')
    plt.title('Performance Metrics Comparison', fontsize=14)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    return plt.gcf()

def main():
    # Read and process data
    df = pd.read_csv('data/players_data-2024_2025.csv')
    combined_df = combine_player_stats(df)
    
    # Filter for forwards
    forwards = combined_df[
        (combined_df['Pos'].str.contains('FW')) &
        (combined_df['90s'] >= 15) &
        (combined_df['Age'] < 28) &
        (combined_df['Gls'] >= 10)
    ].copy()
    
    forwards['Suitability_Score'] = forwards.apply(calculate_striker_suitability, axis=1)
    top_strikers = forwards.nlargest(5, 'Suitability_Score')
    
    # Create visualizations
    radar_chart = create_radar_chart(top_strikers, 'Top 5 Strikers Performance Profile')
    goals_xg_scatter = create_goals_vs_xg_scatter(forwards)
    shot_quality_heatmap = create_shot_quality_heatmap(forwards)
    performance_comparison = create_performance_comparison(top_strikers)
    
    # Save visualizations
    radar_chart.savefig('output/radar_chart.png', dpi=300, bbox_inches='tight')
    goals_xg_scatter.savefig('output/goals_xg_scatter.png', dpi=300, bbox_inches='tight')
    shot_quality_heatmap.savefig('output/shot_quality_heatmap.png', dpi=300, bbox_inches='tight')
    performance_comparison.savefig('output/performance_comparison.png', dpi=300, bbox_inches='tight')
    
    # Generate statistical summary
    summary_stats = forwards[['Player', 'Age', 'Gls', 'xG', 'Goals_per_90', 'Shots_per_90', 'SoT%', 'Suitability_Score']].round(2)
    summary_stats.to_csv('output/striker_summary_stats.csv', index=False)
    
    # Print analysis
    print("\nStriker Analysis Summary:")
    print("=" * 50)
    print("\nTop 5 Strikers by Suitability Score:")
    for _, player in top_strikers.iterrows():
        print(f"\n{player['Player']} (Age: {player['Age']})")
        print(f"Current Team: {player['Squad']}")
        print(f"Goals: {player['Gls']} (xG: {player['xG']:.2f})")
        print(f"Goals per 90: {player['Goals_per_90']:.2f}")
        print(f"Shot Accuracy: {player['SoT%']:.1f}%")
        print(f"Suitability Score: {player['Suitability_Score']:.2f}")
    
    print("\nKey Insights:")
    print("1. Goals vs xG Analysis:")
    print("   - Players above the diagonal line are outperforming their expected goals")
    print("   - Players below the line are underperforming their expected goals")
    
    print("\n2. Shot Quality Metrics:")
    print("   - Higher correlation between Goals per 90 and xG indicates consistent finishing")
    print("   - Shot accuracy (SoT%) shows how clinical the strikers are")
    
    print("\n3. Performance Profile:")
    print("   - Radar charts show balanced performance across key metrics")
    print("   - Larger areas indicate more well-rounded strikers")

if __name__ == "__main__":
    main() 