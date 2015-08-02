import pandas as pd
import matplotlib.pyplot as plt

# Load and setup data
df = pd.DataFrame.from_csv('./../data/nbaallelo.csv')
df['game_result'] = (df['game_result'] == 'W').astype(int)
df['total_ppg'] = df['pts'] + df['opp_pts']

# Figure 1

home_court_adv = df.loc[(df['game_location']=='H')].groupby('year_id')['game_result'].mean()
print "Plotting home_court_adv"
home_court_adv.plot()
plt.xlabel('Year')
plt.ylabel('Home Team Win %')
plt.title('Home Court Advantage Through the Years')
plt.show()

# Figure 2
print "Plotting game_by_game_ppg"
game_by_game_ppg = df.groupby('seasongame')['total_ppg'].mean()
game_by_game_ppg.plot()
plt.xlabel('Game # in Season')
plt.ylabel('Combined Score')
plt.title('Total Game Score Across the NBA Season')
plt.show()

# Figure 3
print "Plotting total_ppg"
total_ppg = df.groupby('year_id')['total_ppg'].mean()
total_ppg.plot()
plt.xlabel('Year')
plt.ylabel('Combined Score')
plt.title('Total Game Score Through the Years')
plt.show()

# Figure 4
print "Plotting ppg_regular_season and ppg_playoffs"
ppg_regular_season = df.loc[(df['is_playoffs'] == False)].groupby('year_id')['total_ppg'].mean()
ppg_playoffs = df.loc[(df['is_playoffs'] == True)].groupby('year_id')['total_ppg'].mean()
ppg_regular_season.plot(label='Regular Season')
ppg_playoffs.plot(label='Playoffs')
plt.xlabel('Year')
plt.ylabel('Combined Score')
plt.legend(loc=9, bbox_to_anchor=(0.5, 0.1), ncol=2)
plt.title('Total Game Score Through the Years')
plt.show()