import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from arsenal_striker_analysis import combine_player_stats, calculate_striker_suitability
import seaborn as sns
import os

# Set the style for all plots
plt.style.use('default')
sns.set_theme()

# Ensure output directory exists
os.makedirs('output', exist_ok=True)

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

def create_distribution_plots(df, metrics, title_prefix):
    for metric in metrics:
        plt.figure(figsize=(10, 6))
        sns.histplot(df[metric], kde=True, bins=30, color='skyblue')
        plt.title(f'{title_prefix} Distribution: {metric}')
        plt.xlabel(metric)
        plt.ylabel('Frequency')
        plt.tight_layout()
        plt.savefig(f'output/dist_{metric}.png', dpi=200)
        plt.close()

def create_boxplots(df, metrics, title_prefix):
    for metric in metrics:
        plt.figure(figsize=(10, 6))
        sns.boxplot(y=df[metric], color='lightgreen')
        plt.title(f'{title_prefix} Boxplot: {metric}')
        plt.ylabel(metric)
        plt.tight_layout()
        plt.savefig(f'output/box_{metric}.png', dpi=200)
        plt.close()

def create_pairplot(df, metrics):
    sns.pairplot(df[metrics], diag_kind='kde')
    plt.suptitle('Pairplot of Key Metrics', y=1.02)
    plt.savefig('output/pairplot_metrics.png', dpi=200, bbox_inches='tight')
    plt.close()

def create_top10_barplots(df, metrics):
    for metric in metrics:
        top10 = df.nlargest(10, metric)
        plt.figure(figsize=(12, 6))
        sns.barplot(x='Player', y=metric, data=top10, palette='viridis')
        plt.title(f'Top 10 Players by {metric}')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(f'output/top10_{metric}.png', dpi=200)
        plt.close()

def save_csv_preview_image(csv_path, out_path, nrows=20):
    df = pd.read_csv(csv_path, nrows=nrows)
    fig, ax = plt.subplots(figsize=(min(20, 2+len(df.columns)//3), 1+nrows//2))
    ax.axis('off')
    tbl = ax.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='center', fontsize=10)
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(8)
    tbl.scale(1, 1.2)
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.close()

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
    top_strikers = forwards.nlargest(10, 'Suitability_Score')
    
    # Key metrics for more detailed analysis
    metrics = ['Gls', 'xG', 'Goals_per_90', 'Shots_per_90', 'SoT%', 'Ast', 'Min', 'Suitability_Score']

    # More visualizations
    create_distribution_plots(forwards, metrics, 'Forwards')
    create_boxplots(forwards, metrics, 'Forwards')
    create_pairplot(forwards, metrics)
    create_top10_barplots(forwards, metrics)

    # Create visualizations
    radar_chart = create_radar_chart(top_strikers.head(5), 'Top 5 Strikers Performance Profile')
    goals_xg_scatter = create_goals_vs_xg_scatter(forwards)
    shot_quality_heatmap = create_shot_quality_heatmap(forwards)
    performance_comparison = create_performance_comparison(top_strikers.head(5))
    
    # Save visualizations
    radar_chart.savefig('output/radar_chart.png', dpi=300, bbox_inches='tight')
    goals_xg_scatter.savefig('output/goals_xg_scatter.png', dpi=300, bbox_inches='tight')
    shot_quality_heatmap.savefig('output/shot_quality_heatmap.png', dpi=300, bbox_inches='tight')
    performance_comparison.savefig('output/performance_comparison.png', dpi=300, bbox_inches='tight')
    
    # Save summary and preview tables
    summary_cols = ['Player', 'Age', 'Min', 'Gls', 'Ast', 'xG', 'Goals_per_90', 'Shots_per_90', 'SoT%', 'Suitability_Score']
    summary_stats = forwards[summary_cols].round(2)
    summary_stats.to_csv('output/striker_summary_stats.csv', index=False)
    summary_stats.head(20).to_html('output/striker_summary_stats.html', index=False)
    summary_stats.head(20).to_markdown('output/striker_summary_stats.md', index=False)

    # Save CSV preview image for README/report
    save_csv_preview_image('data/players_data-2024_2025.csv', 'output/csv_preview.png', nrows=20)

    print("\nDetailed Striker Analysis Report Generated!")
    print("- All visualizations and tables saved in the output/ directory.")
    print("- Preview of player data CSV and summary tables included.")
    print("- See README for updated visualizations and data transparency.")

if __name__ == "__main__":
    main() 