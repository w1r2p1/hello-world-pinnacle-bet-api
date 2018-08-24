import time

import sys
sys.path.append("..") # Adds higher directory to python modules path.

from settings import *

def get_info_event(api, event_id):
    """Get more info about an event.
    """
    fixture = api.market_data.get_fixtures(sport_id=SPORT_ID, league_ids=None, since=None, is_live=None, event_ids=event_id)
    return (fixture['league'][0]['events'][0]['home'] + ' - ' + fixture['league'][0]['events'][0]['away'])

def get_event_live(api, event_id):
    """Get if a event is live or not.
    Return None if event is not live;
    Return {'id': xx, 'state': 3, 'elapsed': num_minutes}
    """
    inrunning = api.market_data.get_inrunning()
    for s in inrunning['sports']: # deportes
        if s['id'] == SPORT_ID: # deporte elegido
            for l in s['leagues']: # ligas
                for e in l['events']: # partidos
                    if e['id'] == event_id:
                        return e
    return None
