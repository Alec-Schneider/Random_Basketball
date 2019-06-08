#! /usr/bin/python3.7

import pandas as pd
from Stats import Stats
from datetime import datetime

# Link of advanced stats from basketball reference
link = 'https://www.basketball-reference.com/leagues/NBA_2019_advanced.html'

# Fetch the data and create a df from the list it returns
data = pd.DataFrame(pd.read_html(link)[0])

# cols to convert and get leader of
stat_cols = ['Rk', 'Age', 'G', 'MP', 'PER', 'TS%', '3PAr',
        'FTr', 'ORB%', 'DRB%', 'TRB%', 'AST%', 'STL%',
        'BLK%', 'TOV%', 'USG%', 'OWS', 'DWS', 'WS', 'WS/48',
        'OBPM', 'DBPM', 'BPM', 'VORP']

month_dict = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
              7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}

# Create up to date file name based off of run day
month = month_dict[datetime.today().month]
day = datetime.today().day
year = datetime.today().year

file = 'AdvdLeaders%s_%s_%s.txt' % (month, day, year)

# Create instance of Stats
x = Stats(data)

# Drop rows that are header rows made for website viewing
# Drop "Unnamed" cols
# Convert stat_cols to floats for analysis
x.clean_df(stat_cols)

# Find best and worst in the league in stats_cols (excluding Rk and Age)
x.league_leader(stat_cols[2:], file, mins=1000)
