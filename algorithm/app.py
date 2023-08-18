import pywebio.pin as pin
from pywebio.output import *
from pywebio import start_server
from algorithm.predict import *

def page():

    img = open('../static_files/images/image_1.png', 'rb').read()
    put_image(img, width='100%', height ='120px')

    # get team names
    home_options, away_options = get_team_name()

    # Team select
    put_row(
        [pin.put_select("hometeam", options=home_options, label='HomeTeam:'), None,
         pin.put_select("awayteam", options=away_options, label='AwayTeam:')],
        size = '47% 6% 47%'
    ).show()

    put_row(
        [pin.put_slider('FTHG', label="FTHG:",value=0, min_value=0, max_value=100, step=1), None,
         pin.put_slider('FTAG', label="FTAG:",value=0, min_value=0, max_value=100, step=1)],
        size = '47% 6% 47%'
    )

    put_row(
        [pin.put_slider('HTHG', label="HTHG:",value=0, min_value=0, max_value=100, step=1), None,
         pin.put_slider('HTAG', label="HTAG:",value=0, min_value=0, max_value=100, step=1)],
        size = '47% 6% 47%'
    )

    put_row(
        [pin.put_slider('HS', label="Shots:",value=0, min_value=0, max_value=100, step=1), None,
         pin.put_slider('AS', label="Shots:",value=0, min_value=0, max_value=100, step=1)],
        size = '47% 6% 47%'
    )

    put_row(
        [pin.put_slider('HST', label="Shots on target:",value=0, min_value=0, max_value=100, step=1), None,
         pin.put_slider('AST', label="Shots on target:",value=0, min_value=0, max_value=100, step=1)],
        size = '47% 6% 47%'
    )
    # yellow card
    put_row(
        [pin.put_slider('HY', label="Yellow Card:  ",value=0, min_value=0, max_value=100, step=1), None,
         pin.put_slider('AY', label="Yellow Card:  ",value=0, min_value=0, max_value=100, step=1)],
        size = '47% 6% 47%'
    )
    # red card
    put_row(
        [pin.put_slider('HR', label="Red Cards:  ",value=0, min_value=0, max_value=100, step=1), None,
         pin.put_slider('AR', label="Red Cards:  ",value=0, min_value=0, max_value=100, step=1)],
        size = '47% 6% 47%'
    )
    put_row([None, put_buttons(["Predict"], lambda _: cal_prob()), None], size = '45% 100% 45%')


def cal_prob():
    if pin.pin['hometeam'] == pin.pin['awayteam']:
        popup('Warning', [
            put_html('<h3>AwayTeam and HomeTeam can not be the same</h3>'),
        ])
        return None


    input_data = {
        'HomeTeam': pin.pin['hometeam'],
        'AwayTeam': pin.pin['awayteam'],
        'FTHG': pin.pin['FTHG'],
        'FTAG': pin.pin['FTAG'],
        'HTHG': pin.pin['HTHG'],
        'HTAG': pin.pin['HTAG'],
        'HS': pin.pin['HS'],
        'AS': pin.pin['AS'],
        'HST': pin.pin['HST'],
        'AST': pin.pin['AST'],
        'HY': pin.pin['HY'],
        'AY': pin.pin['AY'],
        'HR': pin.pin['HR'],
        'AR': pin.pin['AR']
    }
    result = predict(input_data)


    with use_scope('result', clear=True):
        # show the predict win probability of each team
        probs = result['probs']
        put_progressbar('home_win', probs['H'], label='Home Win')
        put_text(str(round(probs['H']*100, 2)) + '%')
        put_progressbar('away_win', probs['A'], label='Away Win')
        put_text(str(round(probs['A']*100, 2)) + '%')
        put_progressbar('draw', probs['D'], label='Draw')
        put_text(str(round(probs['D']*100, 2)) + '%')

        # show the predict odd of each team
        odds = result['odds']
        put_grid([
            [put_text('Home Odd'), put_text('Away Odd'), put_text('Draw Odd')],
            [put_text(odds['H']), put_text(odds['A']), put_text(odds['D'])],
        ], cell_width='33%', cell_height='50px')


if __name__ == "__main__":
    start_server(page, port=8080)