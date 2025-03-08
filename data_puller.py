'''
authors:        Samson Chow 
date created:   Feb. 27, 2025
purpose:        The purpose of this file is to use basketball_reference_web_scraper to get
                game data of the bucks, mavs, and lakers for all games from years 20xx - 20xx
'''

from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import Team
from basketball_reference_web_scraper.data import OutputType
import os
import time
import random

DELAY_TIME = random.randint(3,5)
DIRECTORY = os.getcwd()

# get the season schedule for the three teams so we know the dates where they played
def get_season_schedule(year: int, team: object) ->list:
    '''
    a helper fucntion that has inputs of year and team name
    returns all of the dates played in the season as a list of tuples dates in format (YYYY, MM, DD)
    '''

    print(f'fetching games played for year {year}')

    # return data
    dates_played = []

    # fetch all the data first
    raw_data = client.season_schedule(season_end_year=year)

    # parse through data, look for team and append game to list
    for game in raw_data:
        if game['home_team'] == team or game['away_team'] == team:
            raw_date = str(game['start_time'])
            dates_played.append((int(raw_date[:4]), int(raw_date[5:7]), int(raw_date[8:10])))

    print(f'finished fetching games played for year {year}')
    time.sleep(DELAY_TIME)

    return dates_played

# given a team, this function will fetch all data of all games from the years given 
def get_team_data(team: object, team_name: str, start_year: int, end_year:int) -> None:
    '''
    This function will take in team (object), team_name (string for directory), 
    start year, end year and fetch data of all games from years given
    This function will write to a file, if the directory does not exist, it will create one
    Function returns 0 if everything works, returns error code if not
    '''

    start = time.time()

    # creates team directory if it does not exist
    if not os.path.exists(DIRECTORY + f'/data/{team_name}'):
            path = os.path.join(DIRECTORY + '/data', team_name)
            os.mkdir(path)

            print(f'created directory for {team_name}')

    # loop through all years, use helper function and then write to json file
    for year in range(start_year, end_year + 1):

        sub_start = time.time()

        # create year directory if it does not exist
        if not os.path.exists(DIRECTORY + f'/data/{team_name}/{year}'):
            path = os.path.join(DIRECTORY + f'/data/{team_name}', str(year))
            os.mkdir(path)

            print(f'created directory for {year}')
        else:
            continue
        
        # track what game we are on for the directory
        game_count = 1
        season_schedule = get_season_schedule(year=year, team=team)

        # loop through each game, create JSON file with data
        for game in season_schedule:
            try:
                client.player_box_scores(day=game[2], month=game[1], year=game[0],
                                        output_type=OutputType.CSV,
                                        output_file_path=DIRECTORY + f'/data/{team_name}/{year}/game{game_count}_date{str(game[0]) + str(game[1]) + str(game[2])}.CSV')
                print(f'created data for {team_name}, {year}, game {game_count}')
                game_count += 1
                time.sleep(DELAY_TIME)
            except:
                print('an error has occured!')
                return
        
        sub_end = time.time()
        print(f'year {year} finished in {sub_end - sub_start} seconds')
    

    end = time.time()
    print(f'process completed in {end - start} seconds')

if __name__ == '__main__':
    # can replace team with any team object, and change years
    for team in Team:
        get_team_data(team, team.value.lower().replace(" ", "_"), 2014, 2024)








