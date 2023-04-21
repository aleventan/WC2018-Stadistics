"""
Created on Sun Aug 28 22:00:33 2022

@author: Flia
"""
import json
import os



def openJsonMatches():
    # Competition id for World Cup is 43
    competition_id = 43
    # Load the list of matches for this competition
    with open('Statsbomb/data/matches/' + str(competition_id) + '/3.json') as f:
        matches = json.load(f)
    return matches


def getIdMatch(selected_team):
    op = openJsonMatches()
    match_id = 0
    list_of_dates = []
    list_of_ids = []
    list_of_stage = []
    list_htn = []
    list_atn = []
    list_home_score = []
    list_away_score = []
    for match in op:
        home_team_name = match['home_team']['home_team_name']
        away_team_name = match['away_team']['away_team_name']
        # Check if the selected team appear in the match, and save the data and id in separated list
        if (home_team_name == selected_team) or (away_team_name == selected_team):
            match_id = match['match_id']
            match_date = match['match_date']
            competition_stage = match['competition_stage']['name']
            htn = match['home_team']['home_team_name']
            atn = match['away_team']['away_team_name']
            home_score = match['home_score']
            away_score = match['away_score']

            list_of_ids.append(match_id)
            list_of_dates.append(match_date)
            list_of_stage.append(competition_stage)
            list_htn.append(htn)
            list_atn.append(atn)
            list_home_score.append(home_score)
            list_away_score.append(away_score)

    return list_of_ids, list_of_dates, list_of_stage, list_htn, list_atn, list_home_score, list_away_score


def teamList():
    op = openJsonMatches()
    list_of_teams = []
    # Add a team name to a list
    for team in op:
        team_name = team['home_team']['home_team_name']
        if team_name in list_of_teams:
            pass
        else:
            list_of_teams.append(team_name)
    list_of_teams.sort()
    return list_of_teams

def teamColors(selected_team):
    # Depend on the selected team, then choose the colours
    if selected_team == 'Argentina':
        team_color = 'SkyBlue'
        text_team_color = 'White'
    elif selected_team == 'Australia':
        team_color = 'ForestGreen'
        text_team_color = 'Black'
    elif selected_team == 'Belgium':
        team_color = 'FireBrick'
        text_team_color = 'White'
    elif selected_team == 'Brazil':
        team_color = 'Gold'
        text_team_color = 'Black'
    elif selected_team == 'Colombia':
        team_color = 'Yellow'
        text_team_color = 'Black'
    elif selected_team == 'Costa Rica':
        team_color = 'DarkMagenta'
        text_team_color = 'White'
    elif selected_team == 'Croatia':
        team_color = 'IndianRed'
        text_team_color = 'White'
    elif selected_team == 'Denmark':
        team_color = 'Crimson'
        text_team_color = 'White'
    elif selected_team == 'Egypt':
        team_color = 'LavenderBlush'
        text_team_color = 'Black'
    elif selected_team == 'England':
        team_color = 'White'
        text_team_color = 'Black'
    elif selected_team == 'France':
        team_color = 'Blue'
        text_team_color = 'White'
    elif selected_team == 'Germany':
        team_color = 'LightSeaGreen'
        text_team_color = 'Black'
    elif selected_team == 'Iceland':
        team_color = 'MediumSlateBlue'
        text_team_color = 'White'
    elif selected_team == 'Iran':
        team_color = 'MistyRose'
        text_team_color = 'Black'
    elif selected_team == 'Japan':
        team_color = 'MediumBlue'
        text_team_color = 'White'
    elif selected_team == 'Mexico':
        team_color = 'DarkOliveGreen'
        text_team_color = 'Black'
    elif selected_team == 'Morocco':
        team_color = 'SaddleBrown'
        text_team_color = 'White'
    elif selected_team == 'Nigeria':
        team_color = 'Wheat'
        text_team_color = 'Black'
    elif selected_team == 'Panama':
        team_color = 'Fuchsia'
        text_team_color = 'Black'
    elif selected_team == 'Peru':
        team_color = 'FireBrick'
        text_team_color = 'White'
    elif selected_team == 'Poland':
        team_color = 'LightCyan'
        text_team_color = 'Black'
    elif selected_team == 'Portugal':
        team_color = 'OrangeRed'
        text_team_color = 'Black'
    elif selected_team == 'Russia':
        team_color = 'RebeccaPurple'
        text_team_color = 'White'
    elif selected_team == 'Saudi Arabia':
        team_color = 'DarkKhaki'
        text_team_color = 'Black'
    elif selected_team == 'Senegal':
        team_color = 'ForestGreen'
        text_team_color = 'White'
    elif selected_team == 'Serbia':
        team_color = 'SteelBlue'
        text_team_color = 'Black'
    elif selected_team == 'South Korea':
        team_color = 'Snow'
        text_team_color = 'Black'
    elif selected_team == 'Spain':
        team_color = 'DarkRed'
        text_team_color = 'White'
    elif selected_team == 'Sweden':
        team_color = 'GreenYellow'
        text_team_color = 'Black'
    elif selected_team == 'Switzerland':
        team_color = 'MediumVioletRed'
        text_team_color = 'White'
    elif selected_team == 'Tunisia':
        team_color = 'Maroon'
        text_team_color = 'White'
    elif selected_team == 'Uruguay':
        team_color = 'Aqua'
        text_team_color = 'Black'
    else:
        team_color = 'Black'
        text_team_color = 'White'

    return team_color, text_team_color


if __name__ == "__main__":
    teams = teamList()
    list_unique_id = []
    for team in teams:
        ids = getIdMatch(team)
        id_team = ids[0]
        for id in id_team:
            if id in list_unique_id:
                pass
            else:
                id = str(id) + '.json'
                list_unique_id.append(id)
    # for iid in list_unique_id:
    #     print(iid)

    # Ruta de la carpeta que deseas limpiar
    ruta_carpeta = "Statsbomb\data\three-sixty"

    # Lista de archivos que no deseas borrar
    # archivos_a_mantener = ["archivo1.txt", "archivo2.png", "archivo3.pdf"]

    # Itera sobre todos los archivos en la carpeta y borra aquellos que no estén en la lista
    for archivo in os.listdir(ruta_carpeta):
        if archivo not in list_unique_id:
            os.remove(os.path.join(ruta_carpeta, archivo))

    # print(getIdMatch("Croatia"))
    #print(teamList())
    # team =
    #print(teamColors('Argentina')[0])
