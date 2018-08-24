from pinnacle.apiclient import APIClient
from pinnacle.enums import OddsFormat, Boolean, WinRiskType, FillType
import time
import pandas as pd

import sys
sys.path.append("..") # Adds higher directory to python modules path.

from utils.wrapper import get_info_event, get_event_live
from settings import *


# Local Settings
MIN_ODD = 1.8
SECONDS_SLEEP = 10
PERIOD = 1
BUY_AVAILABLE = False
STAKE = 5.0
OVER = 0.5
FILE_RESULTS = 'results.csv'


# Authentication
api = APIClient(USERNAME, PASSWORD)
lst_events_betted = [] # Event betted list.


def sleep():
    print('\n \n')
    time.sleep(SECONDS_SLEEP)


# Check Odds
def check_odds():
    list_ids_live = []

    # Get live events (first period)
    inrunning = api.market_data.get_inrunning()
    for s in inrunning['sports']: # iterate sports
        if s['id'] == SPORT_ID: # soccer events
            for l in s['leagues']: # iterate leagues
                for e in l['events']: # iterate events
                    if e['state'] == PERIOD:
                        list_ids_live.append(e['id'])

    print('{} : Analyze {} live events'.format(time.strftime("%Y/%m/%d %H:%M:%S"), len(list_ids_live)))

    if not list_ids_live:
        print("{time} : There is'n any live events to analyze".format(time=time.strftime("%Y/%m/%d %H:%M:%S")))
        sleep()
        return

    # Matching parent id events (LISTA_IDS) and live id events
    list_ids = []
    fixtures = api.market_data.get_fixtures(sport_id=SPORT_ID, league_ids=None, since=None, is_live=None, event_ids=list_ids_live)
    for l in fixtures['league']: # iterate leagues
        for e in l['events']: # iterate events
            if e['parentId'] in LISTA_IDS and e['resultingUnit'] == 'Regular': # discard "Corners" events
                if e['liveStatus'] == 1:
                    if e['status'] == "O" or e['status'] == "I":
                        list_ids.append(e['id'])

    if list_ids:

        # Get odds
        odds = api.market_data.get_odds(sport_id=SPORT_ID, league_ids=None, event_ids=list_ids, since=None, is_live=None)

        for l in odds['leagues']: # iterate leagues
            for e in l['events']: # iterate events
                event_live = get_event_live(api, e['id']) # get if event is live
                if len(e['periods']) > 1 and event_live and e['id'] not in lst_events_betted and e['homeScore'] == 0.0 and e['awayScore'] == 0.0: # 0-0 current match result, first period, event live
                    for total in e['periods'][PERIOD]['totals']: # First period
                        if total['over'] > MIN_ODD and total['points'] == OVER: # Over 0.5 and odd > 1.8
                            info_match = get_info_event(api, e['id']) # get more info about event
                            if BUY_AVAILABLE:
                                # Place bet
                                line_id = e['periods'][PERIOD]['lineId']
                                alt_line_id = None
                                if 'altLineId' in total:
                                    alt_line_id = total['altLineId']
                                result = api.betting.place_bet(sport_id=SPORT_ID, event_id=e['id'], line_id=line_id, period_number=PERIOD, bet_type="TOTAL_POINTS", stake=STAKE, team=None, side="OVER", alt_line_id=alt_line_id, win_risk_stake=WinRiskType.Risk.value, accept_better_line=Boolean.TRUE.name, odds_format=OddsFormat.Decimal.value, fill_type="NORMAL", pitcher1_must_start=None, pitcher2_must_start=None, customer_reference=None)
                            else:
                                print('Bet simulation...')
                                result = ''

                            # Add event to don't bet 2 o more times the same bet
                            lst_events_betted.append(e['id'])

                            # Write results to csv file
                            score = str(e['homeScore']) + ' - ' + str(e['awayScore'])
                            url = str(URL) + str(l['id']) + '/Events/' + str(e['id'])
                            data = [time.strftime("%Y/%m/%d %H:%M:%S"), info_match, event_live['state'], event_live['elapsed'], total['over'], total['under'], e['homeScore'], e['awayScore'], url, result]
                            df2 = pd.DataFrame([data])
                            df2.to_csv(FILE_RESULTS, mode='a', header=False)
                            break

    else:
        print("{time} : No bets availables to analyze".format(time=time.strftime("%Y/%m/%d %H:%M:%S")))

    sleep()

# Analyze
while True:
    check_odds()
