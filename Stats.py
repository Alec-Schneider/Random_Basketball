import pandas as pd


class Stats():
    """Class for a dataframe object (specifically from basketball reference)
    and does various manipulations"""
    def __init__(self, df):
        self.df = df.copy()  # Pass a dataframe object to the class
    
    def drop_headers(self, drop='Rk'):
        """Drop all rows that repeat headers"""
        for num, row in self.df.iterrows():
            if row[drop] == drop:
                self.df.drop(num, axis=0, inplace=True)
        for col in self.df.columns:
            if 'Unnamed' in col:
                self.df.drop(col, axis=1, inplace=True)

    def convert_to_float(self, stats):
        """Converts data to float and fills nan to 0"""
        for i in stats:
            self.df[i] = self.df[i].astype(float).fillna(0)

    def clean_df(self, stats):
        self.drop_headers()
        self.convert_to_float(stats)

    def leader_dict(self, stats):
        """Create dict of {stat column: (index of highest, index of lowest)"""
        maxmin = {}
        for i in stats:
            maxmin[i] = (self.df[i].idxmax(), self.df[i].idxmin())
        return maxmin

    def min_restrict(self, min_mins):
        self.df = self.df[self.df['MP'] >= min_mins]
        return self.df

    def write_leaders(self, file, maxmin, col):
        with open(file, 'w') as f:
            f.write('Current league leaders and worst:\n')
            for key in maxmin.keys():
                f.write('Highest %s in the league is: %s %.2f\n' 
                        % (key, self.df.loc[maxmin[key][0], col],
                           self.df.loc[maxmin[key][0], key]))
                f.write('Lowest %s in the league is %s %.2f\n' 
                        % (key, self.df.loc[maxmin[key][1], col],
                            self.df.loc[maxmin[key][1], key]))

    def find_leaders(self, stat, asc=False):
        """Sort stat cateogry"""
        return self.df.sort_values(stat, ascending=asc)

    def league_leader(self, stats, file, col='Player', mins=0):
        """Find the player with the lowest and highest of a stat
        and write to a file"""
        if mins:
            self.min_restrict(mins)

        maxmin = self.leader_dict(stats)  # Create dict of highest and lowest of stat
        self.write_leaders(file, maxmin, col)