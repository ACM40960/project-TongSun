import yaml
import numpy as np


class Odds:
    def __init__(self):
        self.mean_odd = None
        self.sigma = None
        self.bet_num = None
        self.match_outcome = None
        self.__read_config()

    # read the config file for parameters
    def __read_config(self):
        with open("../static_files/config.yml") as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            self.mean_odd = config["mean_odd"]
            self.sigma = config["sigma"]
            self.bet_num = config["bet_num"]
            self.simulation_bet_num = config["simulation_bet_num"]

    def calculate_odds(self, probs):
        '''
        :param probs: the winning probability of each team
        :return: the odd for each team
        The goal is get 5 cent each bet, so:
        (1/win_prob - x) * win_prob = 0.95 ==> x = 1/win_prob - 0.95/win_prob ==> x=(1-0.95)/win_prob
            expand it using Gaussian distribution, the probability between 0.93 and 0.97, so:
        Aussum the probability is prob， then x = 1/win_prob - prob /win_prob ==> x=(1-prob)/win_prob
        '''
        margin_data = {}
        for key in probs:
            # the implied odd calaulate by the predict prob
            pred_odd = 1/probs[key]
            prob = round(probs[key], 4)

            # using 1 sigma as the boundary
            margin_prob = 0
            while abs(margin_prob - self.mean_odd) > self.sigma:
                margin_prob = round(np.random.normal(self.mean_odd, self.sigma, 1)[0],2)


            if (prob != 0):
                # Adjust the implied odd to include margin
                adjust_odd = (1 - margin_prob)/prob
                # calculate the margin odd
                margin_odd = round(prob * (pred_odd - adjust_odd), 4)
            else:
                # if the winning probability for a team, I set the odd as 1
                margin_odd = 1

            margin_data[key] = {'margin_odd': margin_odd,
                                'prob': prob}

        return margin_data