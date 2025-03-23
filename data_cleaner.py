'''
authors:        Samson Chow 
date created:   March 20, 2025
purpose:        The purpose of this script is to aggregate the data by 
                team and then pull out useful stats and clean the data in 
                preparation for training
'''

import os
from pathlib import Path

import pandas as pd

from team_id_enums import TeamId
from basketball_reference_web_scraper.data import Team

# helper function for returning enum
def get_enum_from_string(enum_class, string_value):
    for member in enum_class:
        if member.value == string_value:
            return member
    return None

# helper funciton for returning name given path (GPT wrote this one)
def extract_team_name_from_path(path):
    # Split the path by directory separator
    path_components = path.split('/')
    
    # Find the component that might contain the team name
    for component in path_components:
        if '_' in component and not component.endswith('.csv'):
            # This looks like it might be a team name
            # Convert from snake_case to readable format
            team_name = component.upper()
            return team_name
    
    return None

# funciton for cleaning a spreadsheet
def clean_data(file_path: str, team: Team) -> pd.DataFrame:
    '''
    This function takes in the file path to one spreadsheet and team.
    This funciton will Group the data by team and return cleaned data
    '''
    # select data that we need
    data = pd.read_csv(file_path)
    data = data[data['team'] == team.value]
    data = data.drop(columns=['slug', 'name', 'location', 'seconds_played', 'plus_minus'])

    if data.empty:
        return None

    # aggregate data, keep team, opponent, and outcome as columns
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

    opponent = data['opponent'].iloc[0]

    # used for calculating useful statistics
    opp_data = pd.read_csv(file_path)
    opp_data = opp_data[opp_data['team'] == opponent]
    opp_data = opp_data.drop(columns=['slug', 'name', 'location', 'seconds_played', 'plus_minus'])
    opp_data = opp_data.groupby(['team', 'opponent', 'outcome'], as_index=False).agg(
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

    # calculate useful statistics
    data['percent_fg_made'] = data['made_field_goals'] / data['attempted_field_goals']
    data['percent_3p_made'] = data['made_three_point_field_goals'] / data['attempted_three_point_field_goals']
    data['percent_ft_made'] = data['made_free_throws'] / data['attempted_free_throws']
    data['ORB'] = data['offensive_rebounds'] / (data['offensive_rebounds'] + opp_data['offensive_rebounds'])
    data['DRB'] = data['defensive_rebounds'] / (data['defensive_rebounds'] + opp_data['defensive_rebounds'])
    data['percent_shots_blocked'] = data['blocks'] / (opp_data['attempted_field_goals'] + opp_data['attempted_three_point_field_goals'])
    data['TOVR'] = data['turnovers'] / (data['attempted_field_goals'] + data['attempted_three_point_field_goals'] + 0.44 * data['attempted_free_throws'] + data['turnovers'])

    # one hot encode the winner
    if data['outcome'].iloc[0] == 'WIN':
        data['team_win'] = 1
        data['opp_win'] = 0
    else:
        data['team_win'] = 0
        data['opp_win'] = 1

    # drop uneccesary columns
    data = data.drop(columns=['made_field_goals', 'made_three_point_field_goals', 'made_free_throws',
                              'offensive_rebounds', 'defensive_rebounds', 'blocks', 'turnovers', 'outcome'])
    
    # swap out team names for team ids
    team_id = TeamId[team.name].value
    opponent = get_enum_from_string(Team, opponent)
    opp_id = TeamId[opponent.name].value
    data.at[0, 'team'] = team_id
    data.at[0, 'opponent'] = opp_id

    # can comment out: add the date of the game
    # data['date'] = file_path[-11:-3]

    # for testing purposes
    # data.to_csv('temp.CSV', index=False)

    return data

if __name__ == '__main__':
    # testing stuff
    
    # fp = os.path.join(os.getcwd(), 'data', 'atlanta_hawks', '2014', 'game2_date2013111.CSV')
    # res = clean_data(fp, Team.ATLANTA_HAWKS)

    # fp = os.path.join(os.getcwd(), 'data', 'atlanta_hawks', '2014', 'game9_date20131116.CSV')
    # tmp = clean_data(fp, Team.ATLANTA_HAWKS)
    # res = pd.concat([res, tmp], ignore_index=True)

    # res.to_csv('tmp.CSV', index=False)


    res = pd.DataFrame()
    data_rd = os.path.join(os.getcwd(), 'data')

    # for each team in data
    for root, dirs, files in os.walk(data_rd):
        for file in files:
            if file.endswith('.CSV'):

                # get the team 
                team = extract_team_name_from_path(root)
                team = Team[team]

                path = os.path.join(root, file)
                
                try: 
                    tmp = clean_data(path, team)
                    if not tmp.empty:
                        res = pd.concat([res, tmp], ignore_index=True)
                except Exception as e:
                    print(f"Error processing {path}: {e}")
    
    res.to_csv('cleaned_data.CSV', index=False)

                








    















