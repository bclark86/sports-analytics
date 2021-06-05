import requests
from tqdm import tqdm
import numpy as np
import pandas as pd


def fetch_season_summary(season: str):
    """
    Query team standings for a given season.

    Parameters
    ----------
    season: str
        The season of interest in form of 'XXXXYYYY' where XXXX is the full
        start year and YYYY is the full end year

    Returns
    -------
    dict
        a dict with summary results
    """
    # dictionary holder for the season
    season_standings = dict()

    # api request
    base_url = 'https://statsapi.web.nhl.com/api/v1/standings/byLeague'
    season_id = f'?season={season}'
    season = requests.get(base_url + season_id)

    try:
        season_records = season.json()['records'][0]

        # extract results
        season_standings['season'] = season_records['season']
        season_standings['num_teams'] = len(season_records['teamRecords'])
        results = [{
            'team': team['team']['name'],
            'gp': team['gamesPlayed'],
            'points': team['points'],
            'points_pct': team['pointsPercentage']
        } for team in season_records['teamRecords']
        ]
        season_standings['standings_df'] = pd.DataFrame(results)
        return season_standings
    except Exception:
        pass


def fetch_season_history(start_season='19171918', end_season='20202021'):
    assert len(start_season) == 8
    assert len(end_season) == 8
    start_season_start = int(start_season[:4])
    start_season_end = int(start_season[-4:])
    end_season_start = int(end_season[:4])
    current_start = start_season_start
    current_end = start_season_end
    all_seasons = list()
    for _ in tqdm(np.arange(start_season_start, end_season_start + 1)):
        season = str(current_start) + str(current_end)
        season_dict = fetch_season_summary(season)
        if season_dict is not None:
            all_seasons.append(season_dict)
        current_start += 1
        current_end += 1
    return all_seasons
