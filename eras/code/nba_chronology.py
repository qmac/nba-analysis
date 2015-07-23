import pandas as pd
import matplotlib.pyplot as plt

# Load and setup data
df = pd.DataFrame.from_csv('./../data/nbaallelo.csv')
df['game_result'] = (df['game_result'] == 'W').astype(int)
df['total_ppg'] = df['pts'] + df['opp_pts']

# Figure 1
home_court_adv = df.loc[(df['game_location']=='H')].groupby('year_id')['game_result'].mean()
print home_court_adv

# Figure 2
total_ppg = df.groupby('year_id')['total_ppg'].mean()
print total_ppg

# Figure 3
game_by_game_ppg = df.groupby('seasongame')['total_ppg'].mean()
print game_by_game_ppg

# Figure 4
ppg_regular_season = df.loc[(df['is_playoffs'] == False)].groupby('year_id')['total_ppg'].mean()
ppg_playoffs = df.loc[(df['is_playoffs'] == True)].groupby('year_id')['total_ppg'].mean()
print ppg_regular_season
print ppg_playoffs