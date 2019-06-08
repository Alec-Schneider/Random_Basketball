import pandas as pd


class Stats(pd.DataFrame):
    """Class for a dataframe object (specifically from basketball reference)
    and does various manipulations"""
  
    @property
    def _constructor(self):
        return Stats
    
    def drop_headers(self):
        """Drop all rows that repeat headers"""
        # Adapt func to look at columns
        # Should drop row if a value in df.columns
        drop = self.columns
        for num, row in self.iterrows():
            if row[0] in drop:
                self.drop(num, axis=0, inplace=True)
        for col in self.columns:
            if 'Unnamed' in col:
                self.drop(col, axis=1, inplace=True)

    def convert_to_float(self, stats):
        """Converts data to float and fills nan to 0"""
        for i in stats:
            self[i] = self[i].astype(float).fillna(0)

    def remove_dup_players(self, ident, col, keep_on):
        rks = []
        dups = []
        for i in self[ident]:
            if i not in rks:
                rks.append(i)
            else:
                dups.append(i)
        for i in dups:
            for num, row in self.iterrows():
                if row[ident] == i:
                    if not row[col] == keep_on:
                        self.drop(num, axis=0, inplace=True)

    def clean_df(self, stats):
        self.drop_headers()
        self.convert_to_float(stats)

    def leader_dict(self, stats):
        """Create dict of {stat column: (index of highest, index of lowest)"""
        maxmin = {}
        for i in stats:
            maxmin[i] = (self[i].idxmax(), self[i].idxmin())
        return maxmin

    def min_restrict(self, min_mins, col='MP'):
        return self[self[col] >= min_mins]

    def write_leaders(self, file, maxmin, col):
        with open(file, 'w') as f:
            f.write('Current league leaders and worst:\n')
            for key in maxmin.keys():
                f.write('Highest %s in the league is: %s %.2f\n' 
                        % (key, self.loc[maxmin[key][0], col],
                           self.loc[maxmin[key][0], key]))
                f.write('Lowest %s in the league is %s %.2f\n' 
                        % (key, self.df.loc[maxmin[key][1], col],
                            self.loc[maxmin[key][1], key]))

    def find_leaders(self, stat, asc=False):
        """Sort stat category"""
        return self.sort_values(stat, ascending=asc)

    def league_leader(self, stats, file, col='Player', mins=0):
        """Find the player with the lowest and highest of a stat
        and write to a file"""
        if mins:
            self.min_restrict(mins)

        maxmin = self.leader_dict(stats)  # Create dict of highest and lowest of stat
        self.write_leaders(file, maxmin, col)