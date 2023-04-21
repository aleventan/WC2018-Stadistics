# -*- coding: utf-8 -*-
"""
Created on Mon Aug 29 01:48:31 2022

@author: Flia
"""
from operator import itemgetter
from game_def import *

def counterStats():
    # Count of the stats
    tl = teamList()
    stats_of_matches = []
    list_of_ids = []
    for selected_team in tl:
        var = getIdMatch(selected_team)
        res = list(zip(*var))
        for r in res:
            id = r[0]
            match_date = r[1]
            if id in list_of_ids:
                # If the id already exist in the list, i  do nothing
                pass
            else:
                list_of_ids.append(id)
                stats_dict = dict()
                for v in var[0]:
                    # Compare and open the correct id file
                    if var[0].index(v) == res.index(r):
                        count_pass_home = count_shot_home = count_block_home = count_interception_home = count_ball_recovery_home = count_corner_home = \
                            count_fouls_committed_home = count_penalties_home = count_possession_home = count_dribble_home = count_shots_on_target_home = 0
                        count_pass_away = count_shot_away = count_block_away = count_interception_away = count_ball_recovery_away = \
                            count_corner_away = count_fouls_committed_away = count_penalties_away = count_possession_away = count_dribble_away = \
                            count_shots_on_target_away = 0

                        with open('Statsbomb/data/events/' + str(v) + '.json', encoding='utf-8') as m:
                            events = json.load(m)
                        for event in events:
                            team_name = event['team']['name']
                            tipo_evento = event['type']['name']
                            minute = event['minute']
                            home_team_name = r[3]
                            away_team_name = r[4]
                            color_home, text_color_home = teamColors(home_team_name)
                            color_away, text_color_away = teamColors(away_team_name)
                            if team_name == r[3]:
                                if tipo_evento == 'Pass':
                                    count_pass_home = count_pass_home + 1
                                    if 'pass' in event:
                                        if 'outcome' in event['pass']:
                                            if event['pass']['outcome']['name'] == 'incomplete':
                                                pass
                                            else:
                                                count_possession_home = count_possession_home +1
                                elif tipo_evento == 'Shot' and minute <= 120:
                                    count_shot_home = count_shot_home + 1
                                    shot_on_t_home = event['shot']['outcome']['name']
                                    if shot_on_t_home == 'Goal' or shot_on_t_home == 'Post' or shot_on_t_home == 'Saved':
                                        count_shots_on_target_home = count_shots_on_target_home + 1
                                elif tipo_evento == 'Block':
                                    count_block_home = count_block_home + 1
                                elif tipo_evento == 'Interception':
                                    count_interception_home = count_interception_home + 1
                                elif tipo_evento == 'Ball Recovery':
                                    count_ball_recovery_home = count_ball_recovery_home + 1
                                    count_possession_home = count_possession_home + 1
                                elif tipo_evento == 'Foul Committed':
                                    count_fouls_committed_home = count_fouls_committed_home + 1
                                elif tipo_evento== 'Carry':
                                    count_possession_home = count_possession_home + 1
                                elif tipo_evento == 'Dribble':
                                    if 'dribble' in event:
                                        if event['dribble']['outcome']['name'] == 'Complete':
                                            count_dribble_home = count_dribble_home + 1
                                            count_possession_home = count_possession_home + 1
                                if "goalkeeper" in event:
                                    if "name" in event['goalkeeper']['type']:
                                        if event['goalkeeper']['type']['name'] == "Penalty Conceded":
                                            #Se suma en uno ya que filtra por equipo que recibe el disparo
                                            if minute <= 120:
                                                pass
                                            else:
                                                count_penalties_away = count_penalties_away + 1
                            else:
                                if tipo_evento == 'Pass':
                                    count_pass_away = count_pass_away + 1
                                    if 'pass' in event:
                                        if 'outcome' in event['pass']:
                                            if event['pass']['outcome']['name'] == 'incomplete':
                                                pass
                                            else:
                                                count_possession_away = count_possession_away +1
                                elif tipo_evento == 'Shot' and minute <= 120:
                                    count_shot_away = count_shot_away + 1
                                    shot_on_t_away = event['shot']['outcome']['name']
                                    if shot_on_t_away == 'Goal' or shot_on_t_away == 'Post' or shot_on_t_away == 'Saved':
                                        count_shots_on_target_away = count_shots_on_target_away + 1
                                elif tipo_evento == 'Block':
                                    count_block_away = count_block_away + 1
                                elif tipo_evento == 'Interception':
                                    count_interception_away = count_interception_away + 1
                                elif tipo_evento == 'Ball Recovery':
                                    count_ball_recovery_away = count_ball_recovery_away + 1
                                    count_possession_away = count_possession_away + 1
                                elif tipo_evento == 'Foul Committed':
                                    count_fouls_committed_away = count_fouls_committed_away + 1
                                elif tipo_evento== 'Carry':
                                    count_possession_away = count_possession_away + 1
                                elif tipo_evento == 'Dribble':
                                    if 'dribble' in event:
                                        if event['dribble']['outcome']['name'] == 'Complete':
                                            count_dribble_away = count_dribble_away + 1
                                            count_possession_away = count_possession_away + 1
                                if "goalkeeper" in event:
                                    if "name" in event['goalkeeper']['type']:
                                        if event['goalkeeper']['type']['name'] == "Penalty Conceded":
                                            if minute <= 120:
                                                pass
                                            else:
                                                count_penalties_home = count_penalties_home + 1

                            if "pass" in event:
                                if 'type' in event['pass']:
                                    corner_patter = event['pass']['type']['name']
                                    if corner_patter == 'Corner':
                                        if team_name == r[3]:
                                            count_corner_home = count_corner_home + 1
                                        else:
                                            count_corner_away = count_corner_away + 1
                        # Calculo de posession
                        total_poss = count_possession_home + count_possession_away
                        count_poss = round((count_possession_home / total_poss) * 100)
                        count_poss_away = round((count_possession_away / total_poss) * 100)
                        stats_dict['id_match'] = id
                        stats_dict['match_date'] = match_date
                        stats_dict['home_team_name'] = home_team_name
                        stats_dict['away_team_name'] = away_team_name
                        stats_dict['count_shot_home'] = count_shot_home
                        stats_dict['count_shot_away'] = count_shot_away
                        stats_dict['count_shots_on_target_home'] = count_shots_on_target_home
                        stats_dict['count_shots_on_target_away'] = count_shots_on_target_away
                        stats_dict['count_pass_home'] = count_pass_home
                        stats_dict['count_pass_away'] = count_pass_away
                        stats_dict['count_ball_recovery_home'] = count_ball_recovery_home
                        stats_dict['count_ball_recovery_away'] = count_ball_recovery_away
                        stats_dict['count_fouls_committed_home'] = count_fouls_committed_home
                        stats_dict['count_fouls_committed_away'] = count_fouls_committed_away
                        stats_dict['count_corner_home'] = count_corner_home
                        stats_dict['count_corner_away'] = count_corner_away
                        stats_dict['count_block_home'] = count_block_home
                        stats_dict['count_block_away'] = count_block_away
                        stats_dict['count_interception_home'] = count_interception_home
                        stats_dict['count_interception_away'] = count_interception_away
                        stats_dict['count_penalties_home'] = count_penalties_home
                        stats_dict['count_penalties_away'] = count_penalties_away
                        stats_dict['count_poss_home'] = count_poss
                        stats_dict['count_poss_away'] = count_poss_away
                        stats_dict['count_dribble_home'] = count_dribble_home
                        stats_dict['count_dribble_away'] = count_dribble_away
                        stats_dict['color_home'] = color_home
                        stats_dict['color_away'] = color_away
                        stats_dict['text_color_home'] = text_color_home
                        stats_dict['text_color_away'] = text_color_away

                        stats_of_matches.append(stats_dict.copy())
    # Sort the list by date
    stats_of_matches.sort(key=itemgetter('match_date'))
    print(stats_of_matches)
    name_file = 'all_matches_stats.json'
    with open(name_file, 'w') as outfile:
        json.dump(stats_of_matches, outfile, ensure_ascii=False, indent=4)
        print("Se creo con éxito " + name_file)

def totalTeamStats():
    # Made a json with data from all the teams
    all_teams = []
    all_dict = dict()
    tl = teamList()
    for selected_team in tl:
        # Start count for every team
        count_total_goals_scored = count_total_goals_conceded = count_total_shots = count_shots_on_target = count_clean_sheets = \
            count_yellow_cards = count_red_cards = avg_yellow_card = avg_red_card = count_poss_team = avg_poss_team = \
            avg_shots = avg_shots_on_target = 0
        color_team, text_color_team = teamColors(selected_team)
        var = getIdMatch(selected_team)
        res = list(zip(*var))
        count_games = len(res)
        with open('all_matches_stats.json', 'r') as all_m:
            matches = json.load(all_m)
            for match in matches:
                if match['home_team_name'] == selected_team:
                    count_poss_team = count_poss_team + match['count_poss_home']
                elif match['away_team_name'] == selected_team:
                    count_poss_team = count_poss_team + match['count_poss_away']
            avg_poss_team = round(count_poss_team / count_games, 2)
            for v in var[0]:
                total_stats_dict = dict()
                for r in res:
                    # Compara los index
                    if var[0].index(v) == res.index(r):
                        if selected_team == r[3]:
                            count_total_goals_scored = count_total_goals_scored + r[5]
                            count_total_goals_conceded = count_total_goals_conceded + r[6]
                            if r[6] == 0:
                                count_clean_sheets = count_clean_sheets + 1
                        elif selected_team == r[4]:
                            count_total_goals_scored = count_total_goals_scored + r[6]
                            count_total_goals_conceded = count_total_goals_conceded + r[5]
                            if r[5] == 0:
                                count_clean_sheets = count_clean_sheets + 1
                        # Every time i save the stage reached, but only save the last
                        stage_reached = r[2]

                        with open('Statsbomb/data/events/' + str(v) + '.json', encoding='utf-8') as m:
                            events = json.load(m)
                        for event in events:
                            team_name = event['team']['name']
                            tipo_evento = event['type']['name']
                            minute = event['minute']
                            if team_name == selected_team:
                                if tipo_evento == 'Shot' and minute <= 120:
                                    count_total_shots = count_total_shots + 1
                                    shot_on_t = event['shot']['outcome']['name']
                                    if shot_on_t == 'Goal' or shot_on_t == 'Post' or shot_on_t == 'Saved':
                                        count_shots_on_target = count_shots_on_target +1
                                if 'foul_committed' in event:
                                    if 'card' in event['foul_committed']:
                                        if event['foul_committed']['card']['name'] == 'Yellow Card':
                                            count_yellow_cards = count_yellow_cards + 1
                                        if event['foul_committed']['card']['name'] == 'Red Card':
                                            count_red_cards = count_red_cards + 1

                avg_goals_scored = round(count_total_goals_scored / count_games, 2)
                avg_goals_conceded = round(count_total_goals_conceded / count_games, 2)
                goal_difference = count_total_goals_scored - count_total_goals_conceded
                avg_yellow_card = round(count_yellow_cards / count_games, 2)
                avg_red_card = round(count_red_cards / count_games, 2)
                avg_shots = round(count_total_shots / count_games, 2)
                avg_shots_on_target = round(count_shots_on_target / count_games, 2)

                total_stats_dict['selected_team'] = selected_team
                total_stats_dict['count_games'] = count_games
                total_stats_dict['stage_reached'] = stage_reached
                total_stats_dict['count_total_goals_scored'] = count_total_goals_scored
                total_stats_dict['avg_goals_scored'] = avg_goals_scored
                total_stats_dict['count_total_goals_conceded'] = count_total_goals_conceded
                total_stats_dict['avg_goals_conceded'] = avg_goals_conceded
                total_stats_dict['goal_difference'] = goal_difference
                total_stats_dict['count_total_shots'] = count_total_shots
                total_stats_dict['avg_shots'] = avg_shots
                total_stats_dict['count_shots_on_target'] = count_shots_on_target
                total_stats_dict['avg_shots_on_target'] = avg_shots_on_target
                total_stats_dict['count_clean_sheets'] = count_clean_sheets
                total_stats_dict['count_yellow_cards'] = count_yellow_cards
                total_stats_dict['avg_yellow_card'] = avg_yellow_card
                total_stats_dict['count_red_cards'] = count_red_cards
                total_stats_dict['avg_red_card'] = avg_red_card
                total_stats_dict['avg_poss_team'] = avg_poss_team
                total_stats_dict['color_team'] = color_team
                total_stats_dict['text_color_team'] = text_color_team
            all_teams.append(total_stats_dict.copy())

    name_file = 'total_stats.json'
    with open(name_file, 'w') as outfile:
        json.dump(all_teams, outfile, ensure_ascii=False, indent=4)
        print("Se creo con éxito " + name_file)

if __name__ == "__main__":
    counterStats()
    #totalTeamStats()
    # print(tts)
    # with open('total_stats.json', 'r') as ffile:
    #     data = json.load(ffile)
    #     #print(data)
    #     for i in data:
    #         print(i.get('selected_team'))
    #         print(i.get('count_games'))
    #print(separeteTeams("Spain"))
    #printStadistics()
    #print(printStadistics())
