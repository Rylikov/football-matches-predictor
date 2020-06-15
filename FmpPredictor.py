# TODO Create predictions: w1, w2, x, x1, x2 AND add own home game factor, number of wins and losts
from FmpStatistic import FmpStatistic

# Home advantage - 16% from statistic


class FmpPredictor:
    def __init__(self, team1, team2):
        self.team1 = team1
        self.team2 = team2

        fmp_statistic = FmpStatistic(team1=self.team1, team2=self.team2)
        statistic = fmp_statistic.get_statistic()

        self.first_team_wins = float(statistic['first_team_wins'])
        self.second_team_wins = float(statistic['second_team_wins'])
        self.draws = float(statistic['draws'])

        self.all_options = {}
        self.home_match_advantage_percent = 0.16

    def home_match_advantage(self, first_team_score):
        return first_team_score * self.home_match_advantage_percent

    def guest_match_disadvantage(self, first_team_score, second_team_score):
        return second_team_score - self.home_match_advantage(first_team_score)

    # def first_win(self):
    # def second_win(self):
    # def draw(self):
    #
    # def first_win_draw(self):
    # def second_win_draw(self):

    def results_accumulator(self, team1, team2):
        self.all_options['first_win'] = team1 + self.home_match_advantage(team1)
        self.all_options['second_win'] = self.guest_match_disadvantage(team1, team2)
        self.all_options['draw'] = self.draws

        self.all_options['first_win_draw'] = self.draws + self.all_options['first_win']
        self.all_options['second_win_draw'] = self.draws + self.all_options['second_win']

        return self.all_options

    def get_predictions(self):
        return self.results_accumulator(self.first_team_wins, self.second_team_wins)

