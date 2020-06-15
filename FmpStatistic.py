import pandas as pd
import numpy as np

# TODO number of wins and losts(win or lost series) in current season


class FmpStatistic:
    def __init__(self, team1, team2):
        # Get all seasons(1992-2018) data from JSON
        self.all_seasons_data = pd.read_json("premier_league_points_1992_2018.json")

        # All years titles
        self.all_seasons_years = ['1992_93', '1993_94', '1994_95', '1996_97', '1997_98', '1998_99', '1999_00',
                                  '2000_01', '2001_02', '2002_03', '2003_04', '2004_05', '2005_06', '2006_07',
                                  '2007_08', '2008_09', '2009_10', '2010_11', '2011_12', '2012_13', '2013_14',
                                  '2014_15', '2015_16', '2016_17', '2017_18']
        self.team1 = team1
        self.team2 = team2

        self.draw = 0
        self.t1 = 0
        self.t2 = 0
        self.seasons_weights = self.get_seasons_weights(self.all_seasons_years)

    def get_seasons_weights(self, seasons):
        seasons_weights = {}

        # 26 evenly(equally) spaced points from 0 to 100; remove 0 and 1
        weights = np.linspace(0, 1, len(seasons) + 2)

        for s in range(0, len(seasons)):
            seasons_weights[seasons[s]] = weights[s + 1]

        return seasons_weights

    def convert_to_percent(self, first_team_weights, second_team_weights, draw_weights):
        sum_of_weights = first_team_weights + second_team_weights + draw_weights
        first_team_percentage = (first_team_weights * 100) / sum_of_weights
        second_team_percentage = (second_team_weights * 100) / sum_of_weights
        draw_percentage = (draw_weights * 100) / sum_of_weights
        return {
            'first_team_wins': format(first_team_percentage, '.2f'),
            'second_team_wins': format(second_team_percentage, '.2f'),
            'draws': format(draw_percentage, '.2f')
        }

    def score_parser(self, result, weight, team_number):
        # TODO move t1, t2, draw - to __init__

        if result[0:1] > result[2:3]:
            if team_number == 1:
                self.t1 += weight
            else:
                self.t2 += weight
        elif result[2:3] > result[0:1]:
            if team_number == 2:
                self.t2 += weight
            else:
                self.t1 += weight
        else:
            self.draw += weight

    def get_statistic(self):
        for s in self.all_seasons_years:
            season = self.all_seasons_data.get(s)
            season_formatted = pd.DataFrame.from_records(season['matches'])
            season_formatted.index = season['teams']
            seasons_weight = self.seasons_weights[s]

            if self.team1 in season_formatted and self.team2 in season_formatted:
                res1 = season_formatted[self.team1][self.team2]
                res2 = season_formatted[self.team2][self.team1]
                # res2 = res2[::-1]

                # {'draws': '23.71', 'first_team_wins': '17.14', 'second_team_wins': '59.15'} // MC - SAUTH

                # Home match of the first ream
                # self.score_parser(res1, seasons_weight, 1)
                if res1[0:1] > res1[2:3]:
                    self.t1 += seasons_weight
                elif res1[2:3] > res1[0:1]:
                    self.t2 += seasons_weight
                else:
                    self.draw += seasons_weight

                # Home match of the second ream
                # self.score_parser(res2, seasons_weight, 2)

                if res2[0:1] > res2[2:3]:
                    self.t2 += seasons_weight
                elif res2[2:3] > res2[0:1]:
                    self.t1 += seasons_weight
                else:
                    self.draw += seasons_weight

        return self.convert_to_percent(self.t1, self.t2, self.draw)
