# Import packages
# from nba_api.stats.endpoints import shotchartdetail => problems with nba_api 
import json
import requests
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

### Do not use that as there's an issue with nba_api use request to get data from nba website
# # Load teams file
# teams = json.loads(requests.get('https://raw.githubusercontent.com/bttmly/nba/master/data/teams.json').text)
# # Load players file
# players = json.loads(requests.get('https://raw.githubusercontent.com/bttmly/nba/master/data/players.json').text)

# # Get team ID based on team name
# def get_team_id(team):
#   for team in teams:
#     if team['teamName'] == team:
#       return team['teamId']
#   return -1
# # Get player ID based on player name
# def get_player_id(first, last):
#   for player in players:
#     if player['firstName'] == first and player['lastName'] == last:
#       return player['playerId']
#   return -1

# # Create JSON request
# shot_json = shotchartdetail.ShotChartDetail(
#             team_id = get_team_id('Golden State Warriors'),
#             player_id = get_player_id('Stephen', 'Curry'),
#             context_measure_simple = 'PTS',
#             season_nullable = '2015-16',
#             season_type_all_star = 'Regular Season')

# # Load data into a Python dictionary
# shot_data = json.loads(shot_json.get_json())

# # Get the relevant data from our dictionary
# relevant_data = shot_data['resultSets'][0]

# headers = relevant_data['headers']
# rows = relevant_data['rowSet']

# # Create pandas DataFrame
# curry_data = pd.DataFrame(rows)
# curry_data.columns = headers

#function to draw the basketball court
def create_court(ax, color):
    # Short corner 3PT lines,   we divide by 10 the size of the basketball floor
    ax.plot([-220, -220], [0, 140], linewidth=2, color=color)
    ax.plot([220, 220], [0, 140], linewidth=2, color=color)
    ax.add_artist(mpl.patches.Arc((0, 140), 440, 315, theta1=0, theta2=180, facecolor='none', edgecolor=color, lw=2))
    
    # Lane and Key
    ax.plot([-80, -80], [0, 190], linewidth=2, color=color)
    ax.plot([80, 80], [0, 190], linewidth=2, color=color)
    ax.plot([-60, -60], [0, 190], linewidth=2, color=color)
    ax.plot([60, 60], [0, 190], linewidth=2, color=color)
    ax.plot([-80, 80], [190, 190], linewidth=2, color=color)
    ax.add_artist(mpl.patches.Circle((0, 190), 60, facecolor='none', edgecolor=color, lw=2))
    
    # Rim
    ax.add_artist(mpl.patches.Circle((0, 60), 15, facecolor='none', edgecolor=color, lw=2))
    
    # Remove ticks
    ax.set_xticks([])
    ax.set_yticks([])
        
    # Set axis limits
    ax.set_xlim(-250, 250)
    ax.set_ylim(0, 470)
    
    # Backboard
    ax.plot([-30, 30], [40, 40], linewidth=2, color=color)

    return ax


#get data from csv
player = 'James Harden'
df = pd.read_csv ('nba_shotchartdetail_2018-19.csv')

#Filter the results for the chosen player
df = (df.loc[df['PLAYER_NAME'] == player])


# General plot parameters
mpl.rcParams['font.size'] = 18
mpl.rcParams['axes.linewidth'] = 2
    
# Draw basketball court
fig = plt.figure(figsize=(4, 3.76))
ax = fig.add_axes([0, 0, 1, 1])


# Plot hexbin of shots
ax.hexbin(df['LOC_X'], df['LOC_Y'] + 60, gridsize=(30, 30), extent=(-300, 300, 0, 940), cmap='Reds')
ax = create_court(ax, 'black')

# Annotate player name and season
title = player + '\n2015-16 Regular Season'

ax.text(0, 1.05, title, transform=ax.transAxes, ha='left', va='baseline')

# Save and show figure
plt.savefig('ShotChart.png', dpi=300, bbox_inches='tight')
plt.show()