import pandas as pd
import numpy as np

def combine_player_stats(df):
    """
    Combine statistics for players who transferred mid-season.
    Returns a dataframe with combined stats for players with multiple entries.
    """
    # Identify columns to sum
    sum_columns = ['Min', 'Gls', 'Ast', 'Sh', 'SoT', 'PrgC', 'PrgP', 'xG', 'xAG', 'G-PK', 'PK', 'PKatt']
    
    # Identify columns to take weighted average (weighted by minutes played)
    weighted_columns = ['SoT%', 'Dist']
    
    # Group by player name and aggregate
    combined_stats = df.groupby('Player').agg({
        'Min': 'sum',
        'Gls': 'sum',
        'Ast': 'sum',
        'Sh': 'sum',
        'SoT': 'sum',
        'PrgC': 'sum',
        'PrgP': 'sum',
        'xG': 'sum',
        'xAG': 'sum',
        'G-PK': 'sum',
        'PK': 'sum',
        'PKatt': 'sum',
        'Age': 'first',  # Take the most recent age
        'Pos': 'first',  # Take the most recent position
        'Squad': lambda x: ' → '.join(x),  # Show transfer history
        'Comp': lambda x: ' → '.join(x),   # Show league history
        'Nation': 'first'
    }).reset_index()
    
    # Calculate derived statistics
    combined_stats['90s'] = combined_stats['Min'] / 90
    combined_stats['Goals_per_90'] = combined_stats['Gls'] / combined_stats['90s']
    combined_stats['Shots_per_90'] = combined_stats['Sh'] / combined_stats['90s']
    combined_stats['SoT%'] = (combined_stats['SoT'] / combined_stats['Sh'] * 100).round(1)
    
    return combined_stats

def calculate_striker_suitability(row):
    """
    Calculate suitability score for a striker based on Arsenal's needs.
    """
    # Key metrics focused on goalscoring
    goal_scoring = row['Gls'] / row['90s'] if row['90s'] > 0 else 0  # Goals per 90
    penalty_box_presence = row['Sh'] / row['90s'] if row['90s'] > 0 else 0  # Shots per 90
    conversion = row['Gls'] / row['Sh'] if row['Sh'] > 0 else 0  # Conversion rate
    shot_quality = row['xG'] / row['Sh'] if row['Sh'] > 0 and pd.notnull(row['xG']) else 0  # Shot quality
    
    # Calculate composite score with heavy emphasis on goalscoring
    score = (
        goal_scoring * 5 +      # Heavily weighted goals per 90
        conversion * 3 +        # Strong emphasis on conversion
        penalty_box_presence +  # Shot volume
        shot_quality * 2        # Quality of chances
    )
    
    return score

def main():
    # Read the CSV file
    df = pd.read_csv('data/players_data-2024_2025.csv')
    
    # Combine stats for players with multiple entries
    combined_df = combine_player_stats(df)
    
    # Define top clubs that would be unlikely to sell
    top_clubs = [
        'Barcelona', 'Real Madrid', 'Bayern Munich', 'Paris S-G',
        'Manchester City', 'Liverpool', 'Inter', 'Atletico Madrid'
    ]
    
    # Filter for pure strikers and goalscorers
    forwards = combined_df[
        (combined_df['Pos'].str.contains('FW')) &  # Must be a forward
        (combined_df['90s'] >= 15) &               # Regular starter
        (combined_df['Age'] < 28) &                # Age ceiling for resale value
        (~combined_df['Squad'].str.contains('|'.join(top_clubs))) &  # Exclude top clubs
        (combined_df['Gls'] >= 10)                 # Proven goalscorer
    ].copy()
    
    # Calculate suitability scores
    forwards['Suitability_Score'] = forwards.apply(calculate_striker_suitability, axis=1)
    
    print("\nTop Goalscoring Strikers Available for Arsenal:")
    print("-" * 100)
    print("Player Analysis (Minimum 15 matches, 10+ goals, combined stats for transfers):")
    print("-" * 100)
    
    # Sort players by suitability score
    goalscorers = forwards.nlargest(5, 'Suitability_Score')
    
    # Display detailed analysis of realistic candidates
    for _, player in goalscorers.iterrows():
        print(f"\nPlayer: {player['Player']}")
        print(f"Age: {player['Age']}")
        print(f"Nationality: {player['Nation']}")
        print(f"Current Team(s): {player['Squad']}")
        
        print(f"\nGoalscoring Metrics:")
        print(f"Goals: {player['Gls']} ({player['Goals_per_90']:.2f} per 90)")
        print(f"Non-Penalty Goals: {player['G-PK']}")
        print(f"Penalties Scored: {player['PK']} from {player['PKatt']} attempts")
        print(f"Shot Accuracy: {player['SoT%']}%")
        print(f"Shots per 90: {player['Shots_per_90']:.2f}")
        print(f"Goals per Shot: {(player['Gls']/player['Sh']):.3f}")
        
        print(f"\nChance Quality:")
        print(f"Expected Goals: {player['xG']:.2f}")
        print(f"Goals vs xG: {(player['Gls'] - player['xG']):.2f}")
        
        print(f"\nPlaying Time:")
        print(f"Minutes: {player['Min']}")
        print(f"Complete 90s: {player['90s']:.1f}")
        
        print(f"\nStriker Profile:")
        print("Finishing: " + ("Elite" if player['Goals_per_90'] > 0.7 else "Very Good" if player['Goals_per_90'] > 0.5 else "Good" if player['Goals_per_90'] > 0.3 else "Average"))
        print("Shot Volume: " + ("High" if player['Shots_per_90'] > 3.5 else "Medium" if player['Shots_per_90'] > 2.5 else "Low"))
        print("Penalty Box Presence: " + ("Strong" if player['Shots_per_90'] > 3 else "Moderate" if player['Shots_per_90'] > 2 else "Limited"))
        print("Conversion Rate: " + ("Excellent" if player['Gls']/player['Sh'] > 0.2 else "Good" if player['Gls']/player['Sh'] > 0.15 else "Average"))
        
        print(f"\nEstimated Value: €{(player['Gls'] * 3000000 + player['90s'] * 200000):.1f}M")
        print(f"Suitability Score: {player['Suitability_Score']:.2f}")
        print("-" * 50)

if __name__ == "__main__":
    main()

print("\nWhy These Strikers Would Suit Arsenal:")
print("-" * 100)
print("1. Proven goalscoring record in top leagues")
print("2. High shot volume and good conversion rates")
print("3. Regular starters with consistent minutes")
print("4. Age profile allows for future development")
print("5. Playing for clubs that might be willing to sell")

# Summary statistics
print("\nSummary of Search Criteria:")
print("-" * 100)
print("Arsenal's Requirements:")
print("1. Age: Under 28 (focus on players who can develop and maintain resale value)")
print("2. Experience: Minimum 15 matches played this season")
print("3. Position: Forward")
print("4. Key Metrics Weighted:")
print("   - Goal scoring efficiency")
print("   - Shot conversion rate")
print("   - Shot volume")
print("   - Shot quality") 