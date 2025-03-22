'''
authors:        Samson Chow 
date created:   March 20, 2025
purpose:        The purpose of this script is to aggregate the data by 
                team and then pull out useful stats and clean the data in 
                preparation for training
'''

import os
from enum import Enum

import pandas as pd

from team_id_enums import TeamId
from basketball_reference_web_scraper.data import Team

# funciton for cleaning a spreadsheet
def clean_data(file_path: str, team: Team) -> None:
    '''
    This function will clean the data of the given team and write it to a new 
    file
    '''
    # select data that we need
    data = pd.read_csv(file_path)

    print(data)
    data = data[data['team'] == team.value]



    data = data.drop(columns=['slug', 'name', 'location', 'seconds_played', 'plus_minus'])

    print(data)

    # aggregate data
    data = data.groupby(['team', 'opponent', 'outcome'], as_index=False).agg(
        made_field_goals = ('made_field_goals', 'sum'),
        attempted_field_goals = ('attempted_field_goals', 'sum'),
        made_three_point_field_goals = ('made_three_point_field_goals', 'sum'),
        attempted_three_point_field_goals = ('attempted_three_point_field_goals', 'sum'),
        made_free_throws = ('made_free_throws', 'sum'),
        attempted_free_throws = ('attempted_free_throws', 'sum'),
        offensive_rebounds = ('offensive_rebounds', 'sum'),
        defensive_rebounds = ('defensive_rebounds', 'sum'),
        assists = ('assists', 'sum'),
        steals = ('steals', 'sum'),
        blocks = ('blocks', 'sum'),
        turnovers = ('turnovers', 'sum'),
        personal_fouls = ('personal_fouls', 'sum'),
        avg_game_score = ('game_score', 'mean')
    )

    # write the data
    data.to_csv(f'cleaned_{team.name}.csv', index=False)

    print(data)

if __name__ == '__main__':
    fp = os.path.join(os.getcwd(), 'data', 'atlanta_hawks', '2014', 'game2_date2013111.CSV')
    clean_data(fp, Team.ATLANTA_HAWKS)






