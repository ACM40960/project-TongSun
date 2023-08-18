from algorithm.dataProcessing import Data
from algorithm.model import Model
from algorithm.oddCalculate import Odds
import json
import numpy as np

# data class
Data = Data()
matches_data = Data.dataReader()
# model
Model = Model(matches_data)
# Odds
Odds = Odds()

HomeTeam = None
AwayTeam = None

# get team name for html
def get_team_name():
    home_names = sorted(set(matches_data['HomeTeam']))
    away_name = sorted(set(matches_data['AwayTeam']))

    return home_names, away_name

# predict the probabilty using the new data from front page
def predict(new_data):
    global HomeTeam, AwayTeam
    HomeTeam = new_data['HomeTeam']
    AwayTeam = new_data['AwayTeam']

    # get classifiers from Model class
    classifier_dict = Model.model()
    acc_dict = {}
    # calculate the accuracy of test data
    for key in classifier_dict:
        classifier = Model.trian(classifier_dict[key])
        acc = Model.test(classifier)
        acc_dict[key] = acc

    # compare and pick a best classifier
    sorted_dict  = dict(sorted(acc_dict.items(), key=lambda item: item[1], reverse=True))
    key = next(iter(sorted_dict))
    classifier = classifier_dict[key]

    # predict the result of new data
    probs = Model.prob(classifier, new_data)
    margin_data = Odds.calculate_odds(probs)
    result = {'probs': probs}
    result['odds'] = {key: margin_data[key]['margin_odd'] for key in margin_data}
    calculate_profit(margin_data)
    return result


def calculate_profit(margin_data):
    house_profit = 0
    for key in margin_data:
        team_data = margin_data[key]
        margin_odd = team_data['margin_odd']
        prob = team_data['prob']
        team_bet_num = round(Odds.simulation_bet_num * np.exp(-1/2 * (margin_odd - Odds.mean_odd)**2 / Odds.sigma**2), 0)
        margin_data[key]['bet_num'] = team_bet_num
        # Calculate house profit
        house_profit = house_profit + round(team_bet_num * (1 - margin_odd * prob), 4)


    # Add new content to the JSON data
    newData = {}
    newData["HomeTeam"] = HomeTeam
    newData["AwayTeam"] = AwayTeam
    newData["HomeOdd"] = margin_data['H']['margin_odd']
    newData["AwayOdd"] = margin_data['A']['margin_odd']
    newData["DrawOdd"] = margin_data['D']['margin_odd']
    newData["HomeWinProb"] = margin_data['H']['prob']
    newData["AwayWinProb"] = margin_data['A']['prob']
    newData["DrawWinProb"] = margin_data['D']['prob']
    newData["HomeBetNum"] = margin_data['H']['bet_num']
    newData["AwayBetNum"] = margin_data['A']['bet_num']
    newData["DrawBetNum"] = margin_data['D']['bet_num']
    newData["Profit"] = house_profit

    # 读取文件中的数据
    with open("../static_files/profit.json", "r", encoding="utf-8") as file:
        exist_data = json.load(file)
        exist_data.append(newData)

    # Write the updated JSON data back to the file
    with open("../static_files/profit.json", "w") as file:
        json.dump(exist_data, file, indent=4)
