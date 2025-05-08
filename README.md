# Arsenal Striker Analysis Project

## Project Overview

This project implements a data-driven analysis system for identifying suitable striker targets for Arsenal FC. Using advanced statistical analysis and visualization techniques, the model evaluates strikers based on various performance metrics including goals, expected goals (xG), shot accuracy, and other key performance indicators. The analysis focuses on the 2024-2025 season data from top European leagues.

## Data Analysis Features

### Key Metrics Analyzed
- Goals and Expected Goals (xG)
- Shot Accuracy and Shot Volume
- Goals per 90 minutes
- Progressive Actions
- Age and Transfer Potential

### Visualization Types
1. **Radar Charts**: Performance profile comparison of top strikers
2. **Goals vs xG Scatter**: Performance vs expectation analysis
3. **Shot Quality Heatmap**: Correlation between shooting metrics
4. **Performance Comparison**: Direct comparison of key statistics

## Sample Visualizations

### Radar Chart Analysis
![Radar Chart](output/radar_chart.png)
*Performance profile comparison of top 5 striker targets*

### Goals vs Expected Goals Analysis
![Goals vs xG](output/goals_xg_scatter.png)
*Comparison of actual goals scored versus expected goals (xG)*

### Shot Quality Analysis
![Shot Quality Heatmap](output/shot_quality_heatmap.png)
*Correlation heatmap of key shooting metrics*

### Performance Metrics Comparison
![Performance Comparison](output/performance_comparison.png)
*Direct comparison of key performance indicators*

## Key Findings

### Top Striker Candidates
1. **Ousmane Dembélé (27)**
   - Goals per 90: 1.14
   - Shot Accuracy: 51.6%
   - xG Performance: +5.4 (21 goals vs 15.60 xG)

2. **Mateo Retegui (26)**
   - Goals per 90: 1.02
   - Shot Accuracy: 31.5%
   - xG Performance: +6.5 (24 goals vs 17.50 xG)

3. **Kylian Mbappé (26)**
   - Goals per 90: 0.85
   - Shot Accuracy: 51.2%
   - xG Performance: +3.5 (24 goals vs 20.50 xG)

### Analysis Insights
- Strong correlation between Goals per 90 and xG
- High shot accuracy indicates clinical finishing
- Age profile (24-27) suitable for long-term value

## Project Structure
```
├── scripts/
│   ├── arsenal_striker_analysis.py    # Main analysis script
│   └── visualize_striker_analysis.py  # Visualization generation
├── data/
│   └── players_data-2024_2025.csv    # Player statistics dataset
├── output/
│   ├── radar_chart.png               # Performance profile visualizations
│   ├── goals_xg_scatter.png          # Goals vs xG analysis
│   ├── shot_quality_heatmap.png      # Correlation analysis
│   ├── performance_comparison.png     # Direct stat comparison
│   └── striker_summary_stats.csv     # Detailed statistics
└── requirements.txt                   # Project dependencies
```

## Installation and Usage

### Setup
1. Clone the repository
2. Create a virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate  # On Windows
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Analysis
1. Run the main analysis:
```bash
python scripts/arsenal_striker_analysis.py
```
2. Generate visualizations:
```bash
python scripts/visualize_striker_analysis.py
```

## Data Sources
- Player statistics sourced from FBref
- 2024-2025 season data from top European leagues
- Focus on forwards under 28 years old with 15+ matches played

## Future Improvements
1. **Data Enhancement**
   - Include more advanced metrics (pressing stats, build-up involvement)
   - Add historical performance trends
   - Include transfer market valuations

2. **Analysis Extensions**
   - Tactical fit analysis
   - League difficulty adjustment
   - Team playing style compatibility

3. **Visualization Enhancements**
   - Interactive dashboards
   - Real-time data updates
   - Comparative league analysis

## License
MIT License

## Author
Jaka Kus 