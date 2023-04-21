import json
import pandas as pd
from game_def import teamList, getIdMatch
from bs4 import BeautifulSoup
from helium import *
from operator import itemgetter
import re

def allPlayers():
    # Make a file for every player that appear into the lineup in every match
    teams = teamList()
    for team in teams:
        # Take the ID for every match of each team
        ids = getIdMatch(team)
        list_all_players = []
        match_played = 0
        for id_match in ids[0]:
            # Open the correct file for every ID
            with open('Statsbomb/data/lineups/' + str(id_match) + '.json', encoding='utf-8') as m:
                events = json.load(m)
                for event in events:
                    team_name = event['team_name']
                    lineup = event['lineup']
                    # Only if the team appear into the event, continue and start a new dictionary for each game.
                    if team_name == team:
                        dict_all_players = dict()
                        for player in lineup:
                            list_id_match = []
                            total_time = 0
                            list_pos = []
                            # If appear player['positions'] means that the player plays the game and start writing into the dict the data
                            if player['positions']:
                                total_time_match = 0
                                match_played = 1
                                player_id = player.get('player_id')
                                player_name = player.get('player_name')
                                player_nickname = player.get('player_nickname')
                                dict_all_players['player_id'] = player_id
                                dict_all_players['player_name'] = player_name
                                dict_all_players['player_nickname'] = player_nickname
                                if player['positions'][0]['position'] == 'Goalkeeper':
                                    dict_all_players['goalkeeper'] = 'yes'
                                else:
                                    dict_all_players['goalkeeper'] = 'no'
                                for pos in player['positions']:
                                    # I take the time and separate for seconds
                                    pos_pla = pos.get('position')
                                    from_pos = pos.get('from')
                                    from_pos = from_pos.split(':')
                                    min_from = int(from_pos[0]) * 60
                                    seg_from = int(from_pos[1])
                                    total_seg_from = min_from + seg_from
                                    to_pos = pos.get('to')
                                    if to_pos:
                                        to_pos = to_pos.split(':')
                                        min_to = int(to_pos[0]) * 60
                                        seg_to = int(to_pos[1])
                                        total_seg_to = min_to + seg_to
                                    else:
                                        total_seg_to = 90 * 60
                                    # And now y take the total minutes
                                    total_time_play = round((total_seg_to - total_seg_from) / 60)
                                    total_time_match = total_time_match + total_time_play
                                    list_pos.append(pos_pla)
                                list_id_match.append(id_match)
                                unique_list_id_match = list(set(list_id_match))
                                # unique_list_pos = list(set(list_pos))
                                dict_all_players['match_played'] = match_played
                                dict_all_players['list_id_match'] = unique_list_id_match
                                dict_all_players['total_time'] = total_time_match
                                dict_all_players['positions'] = list_pos
                                for pl in list_all_players:
                                    # If the player appear in the list of players (meaning that the player already play at least one game)
                                    # updating the values
                                    if player_id in pl.values():
                                        poss = pl.get('positions')
                                        poss.extend(list_pos)
                                        unique_list_pos = list(set(poss))
                                        match_played = pl.get('match_played') + 1
                                        total_time = pl.get('total_time') + total_time_match
                                        pl.get('list_id_match').append(id_match)
                                        unique_list_id_match = list(set(pl.get('list_id_match')))
                                        dict_all_players.update({'list_id_match': unique_list_id_match, 'match_played': match_played,
                                                                 'total_time': total_time, 'positions': unique_list_pos})
                                list_all_players.append(dict_all_players.copy())
        df = pd.DataFrame(list_all_players)
        # Because the list has duplicates, i only leave the last fot every player, that contains the latest data
        df.drop_duplicates(subset=['player_id'], keep='last', inplace=True)
        list_all_players_new = df.to_dict("records")
        name_file = 'players/' + team + '.json'
        # Made a file for every national team
        with open(name_file, 'w', encoding='utf-8') as outfile:
            try:
                json.dump(list_all_players_new, outfile, ensure_ascii=False, indent=4)
                print('Archivo ' + name_file + ' creado')
            except:
                print('Ocurrio un error')

def allPlayersDetails():
    # Completed the detailed stats for every player
    teams = teamList()
    for team in teams:
        # Open teh correct file for every team
        name_file = 'players/' + team + '.json'
        with open(name_file, encoding='utf-8') as m:
            players = json.load(m)
            for player in players:
                player_name = player.get('player_name')
                player_id = player.get('player_id')
                ids = player.get('list_id_match')
                list_pos = []
                # I separated in 2 big groups. Goalkeepers and the rest
                if player.get('goalkeeper') == 'yes':
                    # Counters
                    total_passes_gk = total_passes_inc_gk = penalty_saved_rt_gk = penalty_saved_ps_gk = \
                        total_shots_saved_gk = total_goals_conceded_gk = total_shots_received_gk = total_clean_sheets = 0
                    for id_match in ids:
                        with open('Statsbomb/data/events/' + str(id_match) + '.json', encoding='utf-8') as f:
                            match = json.load(f)
                            # Start with 1 the clean sheet because after that i subtract 1 if have goal conceded
                            match_clean_sheets = 1
                            for event in match:
                                minute = event['minute']
                                tipo_evento = event['type']['name']
                                if tipo_evento == 'Own Goal Against':
                                    if event['team']['name'] == team:
                                        match_clean_sheets = 0
                                        total_goals_conceded_gk = total_goals_conceded_gk + 1
                                        total_shots_received_gk = total_shots_received_gk + 1
                                if 'player' in event:
                                    player_name_event = event['player']['name']
                                    if player_name_event == player_name:
                                        if tipo_evento == 'Pass':
                                            if 'pass' in event:
                                                total_passes_gk = total_passes_gk + 1
                                                if 'outcome' in event['pass']:
                                                    if event['pass']['outcome']['name'] == 'Incomplete':
                                                        total_passes_inc_gk = total_passes_inc_gk + 1
                                        if 'goalkeeper' in event:
                                            goalk_type = event['goalkeeper']['type']['name']
                                            # print(event['goalkeeper'])
                                            if goalk_type == 'Shot Faced' or goalk_type == 'Punch':
                                                total_shots_received_gk = total_shots_received_gk + 1
                                            if goalk_type == 'Shot Saved' and minute <= 120:
                                                total_shots_saved_gk = total_shots_saved_gk + 1
                                                total_shots_received_gk = total_shots_received_gk + 1
                                            if goalk_type == 'Penalty Saved':
                                                if minute >= 120:
                                                    # print(event['period'])
                                                    penalty_saved_ps_gk = penalty_saved_ps_gk + 1
                                                else:
                                                    penalty_saved_rt_gk = penalty_saved_rt_gk + 1
                                                    total_shots_received_gk = total_shots_received_gk + 1
                                            if goalk_type == 'Goal Conceded' or goalk_type == 'Penalty Conceded':
                                                match_clean_sheets = 0
                                                total_goals_conceded_gk = total_goals_conceded_gk + 1
                                                total_shots_received_gk = total_shots_received_gk + 1
                            # Here I start adding the clean sheetes
                            total_clean_sheets = total_clean_sheets + match_clean_sheets
                    # Update the existing dictionary
                    player.update({'total_passes_pl': total_passes_pl, 'total_passes_inc_pl': total_passes_inc_pl,
                                   'penalty_saved_rt_gk': penalty_saved_rt_gk, 'penalty_saved_ps_gk': penalty_saved_ps_gk,
                                   'total_shots_saved_gk': total_shots_saved_gk, 'total_goals_conceded_gk': total_goals_conceded_gk,
                                   'total_shots_received_gk': total_shots_received_gk, 'total_clean_sheets': total_clean_sheets})
                else:
                    # Counters for the rest of players
                    total_shots_pl = total_shots_on_target_pl = total_goals_pl = total_assists_pl = total_yellow_card_pl = \
                        total_red_card_pl = total_passes_pl = total_passes_inc_pl = total_dribble_complete_pl = \
                        total_dribble_incomplete_pl = total_cross_complete_pl = total_cross_incomplete_pl = total_interc_won_pl = \
                        total_interc_lose_pl = total_blocks_pl = total_fouls_committed_pl = total_fouls_won_pl = 0
                    for id_match in ids:
                        with open('Statsbomb/data/events/' + str(id_match) + '.json', encoding='utf-8') as f:
                            match = json.load(f)
                            for event in match:
                                minute = event['minute']
                                tipo_evento = event['type']['name']
                                if 'player' in event:
                                    player_name_event = event['player']['name']
                                    if player_name_event == player_name:
                                        if tipo_evento == 'Shot' and minute <= 120:
                                            total_shots_pl = total_shots_pl + 1
                                            shot_on_t = event['shot']['outcome']['name']
                                            if shot_on_t == 'Goal':
                                                total_goals_pl = total_goals_pl + 1
                                            if shot_on_t == 'Goal' or shot_on_t == 'Post' or shot_on_t == 'Saved':
                                                total_shots_on_target_pl = total_shots_on_target_pl + 1
                                        if tipo_evento == 'Pass':
                                            if 'pass' in event:
                                                total_passes_pl = total_passes_pl + 1
                                                if 'outcome' in event['pass']:
                                                    if event['pass']['outcome']['name'] == 'Incomplete':
                                                        total_passes_inc_pl = total_passes_inc_pl + 1
                                                if 'goal_assist' in event['pass']:
                                                    total_assists_pl = total_assists_pl + 1
                                                if 'cross' in event['pass']:
                                                    if 'outcome' in event['pass']:
                                                        if event['pass']['outcome']['name'] == 'Complete':
                                                            total_cross_complete_pl = total_cross_complete_pl + 1
                                                        else:
                                                            total_cross_incomplete_pl = total_cross_incomplete_pl + 1
                                                    else:
                                                        total_cross_complete_pl = total_cross_complete_pl + 1
                                        if tipo_evento == 'Interception':
                                            interc = event['interception']['outcome']['name']
                                            if interc == 'Won' or interc == 'Success In Play':
                                                total_interc_won_pl = total_interc_won_pl + 1
                                            else:
                                                total_interc_lose_pl = total_interc_lose_pl + 1
                                        if tipo_evento == 'Block':
                                            total_blocks_pl = total_blocks_pl +1
                                        if tipo_evento == 'Foul Committed':
                                            total_fouls_committed_pl = total_fouls_committed_pl + 1
                                        if tipo_evento == 'Foul Won':
                                            total_fouls_won_pl = total_fouls_won_pl + 1
                                        if 'foul_committed' in event:
                                            if 'card' in event['foul_committed']:
                                                if event['foul_committed']['card']['name'] == 'Yellow Card':
                                                    total_yellow_card_pl = total_yellow_card_pl + 1
                                                if event['foul_committed']['card']['name'] == 'Red Card':
                                                    total_red_card_pl = total_red_card_pl + 1
                                        if 'dribble' in event:
                                            total_dribble_complete_pl = total_dribble_complete_pl + 1
                                            if event['dribble']['outcome']['name'] == 'Incomplete':
                                                total_dribble_incomplete_pl = total_dribble_incomplete_pl + 1
                    # Update the existing dictionary
                    player.update({'total_shots': total_shots_pl, 'total_shots_on_target_pl': total_shots_on_target_pl,
                                   'total_goals_pl': total_goals_pl, 'total_assists_pl': total_assists_pl,
                                   'total_yellow_card_pl': total_yellow_card_pl, 'total_red_card_pl': total_red_card_pl,
                                   'total_passes_pl': total_passes_pl, 'total_passes_inc_pl': total_passes_inc_pl,
                                   'total_dribble_complete_pl': total_dribble_complete_pl, 'total_dribble_incomplete_pl': total_dribble_incomplete_pl,
                                   'total_cross_complete_pl': total_cross_complete_pl, 'total_cross_incomplete_pl': total_cross_incomplete_pl,
                                   'total_interc_won_pl': total_interc_won_pl, 'total_interc_lose_pl': total_interc_lose_pl,
                                   'total_blocks_pl': total_blocks_pl, 'total_fouls_committed_pl': total_fouls_committed_pl,
                                   'total_fouls_won_pl': total_fouls_won_pl
                                   })
                # Because the function getImage is heavy, if I already have it, I pass
                if player.get(('img_web')):
                    pass
                else:
                    if player.get('player_nickname'):
                        name_search_web = player.get('player_nickname')
                    else:
                        name_search_web = player.get('player_name')
                    img_web = getImage(name_search_web)
                    player.update({'img_web': img_web})
        # Sort the list with the player name
        players.sort(key=itemgetter('player_name'))
        with open(name_file, 'w', encoding='utf-8') as outfile:
            try:
                json.dump(players, outfile, ensure_ascii=False, indent=4)
                print('Archivo ' + name_file + ' actualizado')
            except:
                print('Ocurrio un error')

def getImage(player):
    # make webscripting and take from transfermarkt the photo of every player
    url = 'https://www.transfermarkt.es/schnellsuche/ergebnis/schnellsuche?query=' + player
    browser = start_chrome(url, headless=True)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    quotes = soup.find_all('img')
    for items in quotes:
        titulo = items.get('title')
        if isinstance(titulo, str):
            if player in titulo:
                small_jpg = items.get('src')
                # when I found the correct photo, replace the size
                new_jpg = small_jpg.replace('small', 'header')
                break
        else:
            continue
    try:
        # If I have success and found the image, continue. If not, make the default photo
        if new_jpg:
            pass
    except NameError:
        new_jpg = 'https://img.a.transfermarkt.technology/portrait/header/default.jpg?lm=1'
    return new_jpg

def allGoalKeepersStats():
    # Made a compression list for every gk
    teams = teamList()
    all_gk = [{
        **player,
        "team_name": team,
        "total_passes_pl": round(player.get("total_passes_pl") / player.get("match_played"), 2),
        "total_passes_inc_pl": round(player.get("total_passes_inc_pl") / player.get("match_played"), 2),
        "penalty_saved_rt_gk": round(player.get("penalty_saved_rt_gk") / player.get("match_played"), 2),
        "penalty_saved_ps_gk": round(player.get("penalty_saved_ps_gk") / player.get("match_played"), 2),
        "total_shots_saved_gk": round(player.get("total_shots_saved_gk") / player.get("match_played"), 2),
        "total_goals_conceded_gk": round(player.get("total_goals_conceded_gk") / player.get("match_played"), 2),
        "total_shots_received_gk": round(player.get("total_shots_received_gk") / player.get("match_played"), 2)
    } for team in teams for player in json.load(open(f'players/{team}.json', encoding='utf-8')) if player.get("goalkeeper") == "yes"]

    name_file = 'all_gk.json'
    with open(name_file, 'w', encoding='utf-8') as outfile:
        try:
            json.dump(all_gk, outfile, ensure_ascii=False, indent=4)
            print('Archivo ' + name_file + ' creado')
        except:
            print('Ocurrio un error')

def graph_all_gk(id_player):
    with open('all_gk.json', 'r', encoding='utf-8') as m:
        all_gks = json.load(m)
        cant_gks = len(all_gks)
        # Counters
        total_avg_match_pl = total_avg_passes_compl = total_avg_passes_incompl = total_avg_penalty_saved_rt_gk = \
        total_avg_penalty_saved_ps_gk = total_avg_shots_saved_gk = total_avg_goals_conceded_gk = total_avg_shots_received_gk = \
        total_avg_clean_sheets = 0
        for gk in all_gks:
            # adding the value to the counter and after that round it
            total_avg_match_pl = total_avg_match_pl + gk.get('match_played')
            total_avg_passes_compl = total_avg_passes_compl + gk.get('total_passes_pl')
            total_avg_passes_incompl = total_avg_passes_incompl + gk.get('total_passes_inc_pl')
            total_avg_penalty_saved_rt_gk = total_avg_penalty_saved_rt_gk + gk.get('penalty_saved_rt_gk')
            total_avg_penalty_saved_ps_gk = total_avg_penalty_saved_ps_gk + gk.get('penalty_saved_ps_gk')
            total_avg_shots_saved_gk = total_avg_shots_saved_gk + gk.get('total_shots_saved_gk')
            total_avg_goals_conceded_gk = total_avg_goals_conceded_gk + gk.get('total_goals_conceded_gk')
            total_avg_shots_received_gk = total_avg_shots_received_gk + gk.get('total_shots_received_gk')
            total_avg_clean_sheets = total_avg_clean_sheets + gk.get('total_clean_sheets')
            # Take the data for the selected gk
            if id_player == gk.get('player_id'):
                if gk.get('player_nickname'):
                    name_player = gk.get('player_nickname')
                else:
                    name_player = gk.get('player_name')
                gk_matches_pl = gk.get('match_played')
                gk_passes_comp = gk.get('total_passes_pl')
                gk_passes_inc = gk.get('total_passes_inc_pl')
                gk_penalty_saved_rt = gk.get('penalty_saved_rt_gk')
                gk_penalty_saved_ps = gk.get('penalty_saved_ps_gk')
                gk_total_shots_saved = gk.get('total_shots_saved_gk')
                gk_total_goals_conceded = gk.get('total_goals_conceded_gk')
                gk_total_shots_received = gk.get('total_shots_received_gk')
                gk_total_clean_sheets = gk.get('total_clean_sheets')
        total_avg_match_pl = round(total_avg_match_pl / cant_gks, 2)
        total_avg_passes_compl = round(total_avg_passes_compl / cant_gks, 2)
        total_avg_passes_incompl = round(total_avg_passes_incompl / cant_gks, 2)
        total_avg_penalty_saved_rt_gk = round(total_avg_penalty_saved_rt_gk / cant_gks, 2)
        total_avg_penalty_saved_ps_gk = round(total_avg_penalty_saved_ps_gk / cant_gks, 2)
        total_avg_shots_saved_gk = round(total_avg_shots_saved_gk / cant_gks, 2)
        total_avg_goals_conceded_gk = round(total_avg_goals_conceded_gk / cant_gks, 2)
        total_avg_shots_received_gk = round(total_avg_shots_received_gk / cant_gks, 2)
        total_avg_clean_sheets = round(total_avg_clean_sheets / cant_gks, 2)

        return name_player, gk_matches_pl, gk_passes_comp, gk_passes_inc, gk_penalty_saved_rt, gk_penalty_saved_ps, \
               gk_total_shots_saved, gk_total_goals_conceded, gk_total_shots_received, gk_total_clean_sheets, \
               total_avg_match_pl, total_avg_passes_compl, total_avg_passes_incompl, total_avg_penalty_saved_rt_gk, \
               total_avg_penalty_saved_ps_gk, total_avg_shots_saved_gk, total_avg_goals_conceded_gk, total_avg_shots_received_gk, \
               total_avg_clean_sheets

def allDefendersStats():
    teams = teamList()
    all_df = []
    for team in teams:
        name_file = 'players/' + team + '.json'
        with open(name_file, encoding='utf-8') as m:
            players = json.load(m)
            for player in players:
                positions = player.get('positions')
                if any("Back" in word for word in positions):
                        single_df = player
                        single_df['team_name'] = team
                        single_df.pop('goalkeeper')
                        single_df.pop('list_id_match')
                        single_df.pop('img_web')
                        count_matches = single_df.get('match_played')
                        single_df['total_shots'] = round(single_df.get('total_shots') / count_matches, 2)
                        single_df['total_shots_on_target_pl'] = round(single_df.get('total_shots_on_target_pl') / count_matches, 2)
                        single_df['total_goals_pl'] = round(single_df.get('total_goals_pl') / count_matches, 2)
                        single_df['total_assists_pl'] = round(single_df.get('total_assists_pl') / count_matches, 2)
                        single_df['total_yellow_card_pl'] = round(single_df.get('total_yellow_card_pl') / count_matches, 2)
                        single_df['total_red_card_pl'] = round(single_df.get('total_red_card_pl') / count_matches, 2)
                        single_df['total_passes_pl'] = round(single_df.get('total_passes_pl') / count_matches, 2)
                        single_df['total_passes_inc_pl'] = round(single_df.get('total_passes_inc_pl') / count_matches, 2)
                        single_df['total_dribble_complete_pl'] = round(single_df.get('total_dribble_complete_pl') / count_matches, 2)
                        single_df['total_dribble_incomplete_pl'] = round(single_df.get('total_dribble_incomplete_pl') / count_matches, 2)
                        single_df['total_cross_complete_pl'] = round(single_df.get('total_cross_complete_pl') / count_matches, 2)
                        single_df['total_cross_incomplete_pl'] = round(single_df.get('total_cross_incomplete_pl') / count_matches, 2)
                        single_df['total_interc_won_pl'] = round(single_df.get('total_interc_won_pl') / count_matches, 2)
                        single_df['total_interc_lose_pl'] = round(single_df.get('total_interc_lose_pl') / count_matches, 2)
                        single_df['total_blocks_pl'] = round(single_df.get('total_blocks_pl') / count_matches, 2)
                        single_df['total_fouls_committed_pl'] = round(single_df.get('total_fouls_committed_pl') / count_matches, 2)
                        single_df['total_fouls_won_pl'] = round(single_df.get('total_fouls_won_pl') / count_matches, 2)

                        all_df.append(single_df.copy())
    name_file = 'all_df.json'
    with open(name_file, 'w', encoding='utf-8') as outfile:
        try:
            json.dump(all_df, outfile, ensure_ascii=False, indent=4)
            print('Archivo ' + name_file + ' creado')
        except:
            print('Ocurrio un error')

def graph_spider_def(id_player):
    with open('all_df.json', 'r', encoding='utf-8') as m:
        all_dfs = json.load(m)
        cant_dfs = len(all_dfs)
        total_avg_match_pl = total_avg_shots = total_avg_total_shots_on_target = total_avg_goals = \
        total_avg_assists = total_avg_yellow_card = total_avg_red_card = total_avg_passes = \
        total_avg_passes_inc = total_avg_dribble_complete = total_avg_dribble_incomplete = total_avg_cross_complete = \
        total_avg_cross_incomplete = total_avg_interc_won = total_avg_interc_lose = \
        total_avg_blocks = total_avg_fouls_committed = total_avg_fouls_won = 0

        for df in all_dfs:
            total_avg_match_pl = total_avg_match_pl + df.get('match_played')
            total_avg_shots = total_avg_shots + df.get('total_shots')
            total_avg_total_shots_on_target = total_avg_total_shots_on_target + df.get('total_shots_on_target_pl')
            total_avg_goals = total_avg_goals + df.get('total_goals_pl')
            total_avg_assists = total_avg_assists + df.get('total_assists_pl')
            total_avg_yellow_card = total_avg_yellow_card + df.get('total_yellow_card_pl')
            total_avg_red_card = total_avg_red_card + df.get('total_red_card_pl')
            total_avg_passes = total_avg_passes + df.get('total_passes_pl')
            total_avg_passes_inc = total_avg_passes_inc + df.get('total_passes_inc_pl')
            total_avg_dribble_complete = total_avg_dribble_complete + df.get('total_dribble_complete_pl')
            total_avg_dribble_incomplete = total_avg_dribble_incomplete + df.get('total_dribble_incomplete_pl')
            total_avg_cross_complete = total_avg_cross_complete + df.get('total_cross_complete_pl')
            total_avg_cross_incomplete = total_avg_cross_incomplete + df.get('total_cross_incomplete_pl')
            total_avg_interc_won = total_avg_interc_won + df.get('total_interc_won_pl')
            total_avg_interc_lose = total_avg_interc_lose + df.get('total_interc_lose_pl')
            total_avg_blocks = total_avg_blocks + df.get('total_blocks_pl')
            total_avg_fouls_committed = total_avg_fouls_committed + df.get('total_fouls_committed_pl')
            total_avg_fouls_won = total_avg_fouls_won + df.get('total_fouls_won_pl')

            if id_player == df.get('player_id'):
                if df.get('player_nickname'):
                    name_player = df.get('player_nickname')
                else:
                    name_player = df.get('player_name')
                df_matches_pl = df.get('match_played')
                df_total_goals = df.get('total_goals_pl')
                df_total_assists = df.get('total_assists_pl')
                df_total_yellow_card = df.get('total_yellow_card_pl')
                df_total_red_card = df.get('total_red_card_pl')
                df_total_cross_complete = df.get('total_cross_complete_pl')
                df_total_cross_incomplete = df.get('total_cross_incomplete_pl')
                df_total_interc_won = df.get('total_interc_won_pl')
                df_total_interc_lose = df.get('total_interc_lose_pl')
                df_total_blocks = df.get('total_blocks_pl')
                df_total_fouls_committed = df.get('total_fouls_committed_pl')
        total_avg_match_pl = round(total_avg_match_pl / cant_dfs, 2)
        total_avg_goals = round(total_avg_goals / cant_dfs, 2)
        total_avg_assists = round(total_avg_assists / cant_dfs, 2)
        total_avg_yellow_card = round(total_avg_yellow_card / cant_dfs, 2)
        total_avg_red_card = round(total_avg_red_card / cant_dfs, 2)
        total_avg_cross_complete = round(total_avg_cross_complete / cant_dfs, 2)
        total_avg_cross_incomplete = round(total_avg_cross_incomplete / cant_dfs, 2)
        total_avg_interc_won = round(total_avg_interc_won / cant_dfs, 2)
        total_avg_interc_lose = round(total_avg_interc_lose / cant_dfs, 2)
        total_avg_blocks = round(total_avg_blocks / cant_dfs, 2)
        total_avg_fouls_committed = round(total_avg_fouls_committed / cant_dfs, 2)

        return name_player, df_matches_pl, df_total_goals, df_total_assists, df_total_yellow_card, df_total_red_card, \
               df_total_cross_complete, df_total_cross_incomplete, df_total_interc_won, \
               df_total_interc_lose, df_total_blocks, df_total_fouls_committed, \
               total_avg_match_pl, total_avg_goals, total_avg_assists, total_avg_yellow_card, total_avg_red_card, \
               total_avg_cross_complete, total_avg_cross_incomplete, total_avg_interc_won, \
               total_avg_interc_lose, total_avg_blocks, total_avg_fouls_committed

def allMidfieldStats():
    teams = teamList()
    all_md = []
    for team in teams:
        name_file = 'players/' + team + '.json'

        with open(name_file, encoding='utf-8') as m:
            players = json.load(m)
            for player in players:
                positions = player.get('positions')
                if any("Midfield" in word for word in positions):
                        single_md = player
                        single_md['team_name'] = team
                        single_md.pop('goalkeeper')
                        single_md.pop('list_id_match')
                        single_md.pop('img_web')
                        count_matches = single_md.get('match_played')
                        single_md['total_shots'] = round(single_md.get('total_shots') / count_matches, 2)
                        single_md['total_shots_on_target_pl'] = round(single_md.get('total_shots_on_target_pl') / count_matches, 2)
                        single_md['total_goals_pl'] = round(single_md.get('total_goals_pl') / count_matches, 2)
                        single_md['total_assists_pl'] = round(single_md.get('total_assists_pl') / count_matches, 2)
                        single_md['total_yellow_card_pl'] = round(single_md.get('total_yellow_card_pl') / count_matches, 2)
                        single_md['total_red_card_pl'] = round(single_md.get('total_red_card_pl') / count_matches, 2)
                        single_md['total_passes_pl'] = round(single_md.get('total_passes_pl') / count_matches, 2)
                        single_md['total_passes_inc_pl'] = round(single_md.get('total_passes_inc_pl') / count_matches, 2)
                        single_md['total_dribble_complete_pl'] = round(single_md.get('total_dribble_complete_pl') / count_matches, 2)
                        single_md['total_dribble_incomplete_pl'] = round(single_md.get('total_dribble_incomplete_pl') / count_matches, 2)
                        single_md['total_cross_complete_pl'] = round(single_md.get('total_cross_complete_pl') / count_matches, 2)
                        single_md['total_cross_incomplete_pl'] = round(single_md.get('total_cross_incomplete_pl') / count_matches, 2)
                        single_md['total_interc_won_pl'] = round(single_md.get('total_interc_won_pl') / count_matches, 2)
                        single_md['total_interc_lose_pl'] = round(single_md.get('total_interc_lose_pl') / count_matches, 2)
                        single_md['total_blocks_pl'] = round(single_md.get('total_blocks_pl') / count_matches, 2)
                        single_md['total_fouls_committed_pl'] = round(single_md.get('total_fouls_committed_pl') / count_matches, 2)
                        single_md['total_fouls_won_pl'] = round(single_md.get('total_fouls_won_pl') / count_matches, 2)

                        all_md.append(single_md.copy())
    name_file = 'all_md.json'
    with open(name_file, 'w', encoding='utf-8') as outfile:
        try:
            json.dump(all_md, outfile, ensure_ascii=False, indent=4)
            print('Archivo ' + name_file + ' creado')
        except:
            print('Ocurrio un error')

def graph_spider_mid(id_player):
    with open('all_md.json', 'r', encoding='utf-8') as m:
        all_mds = json.load(m)
        cant_mds = len(all_mds)
        total_avg_match_pl = total_avg_shots = total_avg_total_shots_on_target = total_avg_goals = \
        total_avg_assists = total_avg_yellow_card = total_avg_red_card = total_avg_passes = \
        total_avg_passes_inc = total_avg_dribble_complete = total_avg_dribble_incomplete = total_avg_cross_complete = \
        total_avg_cross_incomplete = total_avg_interc_won = total_avg_interc_lose = \
        total_avg_blocks = total_avg_fouls_committed = total_avg_fouls_won = 0

        for md in all_mds:
            total_avg_match_pl = total_avg_match_pl + md.get('match_played')
            total_avg_shots = total_avg_shots + md.get('total_shots')
            total_avg_total_shots_on_target = total_avg_total_shots_on_target + md.get('total_shots_on_target_pl')
            total_avg_goals = total_avg_goals + md.get('total_goals_pl')
            total_avg_assists = total_avg_assists + md.get('total_assists_pl')
            total_avg_yellow_card = total_avg_yellow_card + md.get('total_yellow_card_pl')
            total_avg_red_card = total_avg_red_card + md.get('total_red_card_pl')
            total_avg_passes = total_avg_passes + md.get('total_passes_pl')
            total_avg_passes_inc = total_avg_passes_inc + md.get('total_passes_inc_pl')
            total_avg_dribble_complete = total_avg_dribble_complete + md.get('total_dribble_complete_pl')
            total_avg_dribble_incomplete = total_avg_dribble_incomplete + md.get('total_dribble_incomplete_pl')
            total_avg_cross_complete = total_avg_cross_complete + md.get('total_cross_complete_pl')
            total_avg_cross_incomplete = total_avg_cross_incomplete + md.get('total_cross_incomplete_pl')
            total_avg_interc_won = total_avg_interc_won + md.get('total_interc_won_pl')
            total_avg_interc_lose = total_avg_interc_lose + md.get('total_interc_lose_pl')
            total_avg_blocks = total_avg_blocks + md.get('total_blocks_pl')
            total_avg_fouls_committed = total_avg_fouls_committed + md.get('total_fouls_committed_pl')
            total_avg_fouls_won = total_avg_fouls_won + md.get('total_fouls_won_pl')

            if id_player == md.get('player_id'):
                if md.get('player_nickname'):
                    name_player = md.get('player_nickname')
                else:
                    name_player = md.get('player_name')
                md_matches_pl = md.get('match_played')
                md_total_shots = md.get('total_shots')
                md_total_shots_on_target = md.get('total_shots_on_target_pl')
                md_total_goals = md.get('total_goals_pl')
                md_total_assists = md.get('total_assists_pl')
                md_total_yellow_card = md.get('total_yellow_card_pl')
                md_total_red_card = md.get('total_red_card_pl')
                md_total_passes = md.get('total_passes_pl')
                md_total_passes_inc = md.get('total_passes_inc_pl')
                md_total_dribble_complete = md.get('total_dribble_complete_pl')
                md_total_dribble_incomplete = md.get('total_dribble_incomplete_pl')
                md_total_cross_complete = md.get('total_cross_complete_pl')
                md_total_cross_incomplete = md.get('total_cross_incomplete_pl')
                md_total_fouls_committed = md.get('total_fouls_committed_pl')
                md_total_fouls_won = md.get('total_fouls_won_pl')
        total_avg_match_pl = round(total_avg_match_pl / cant_mds, 2)
        total_avg_shots = round(total_avg_shots / cant_mds, 2)
        total_avg_total_shots_on_target = round(total_avg_total_shots_on_target / cant_mds, 2)
        total_avg_goals = round(total_avg_goals / cant_mds, 2)
        total_avg_assists = round(total_avg_assists / cant_mds, 2)
        total_avg_yellow_card = round(total_avg_yellow_card / cant_mds, 2)
        total_avg_red_card = round(total_avg_red_card / cant_mds, 2)
        total_avg_passes = round(total_avg_passes / cant_mds, 2)
        total_avg_passes_inc = round(total_avg_passes_inc / cant_mds, 2)
        total_avg_dribble_complete = round(total_avg_dribble_complete / cant_mds, 2)
        total_avg_dribble_incomplete = round(total_avg_dribble_incomplete / cant_mds, 2)
        total_avg_cross_complete = round(total_avg_cross_complete / cant_mds, 2)
        total_avg_cross_incomplete = round(total_avg_cross_incomplete / cant_mds, 2)
        total_avg_fouls_committed = round(total_avg_fouls_committed / cant_mds, 2)
        total_avg_fouls_won = round(total_avg_fouls_won / cant_mds, 2)

        return name_player, md_matches_pl, md_total_shots, md_total_shots_on_target, md_total_goals, md_total_assists, \
               md_total_yellow_card, md_total_red_card, md_total_passes, md_total_passes_inc, md_total_dribble_complete, \
               md_total_dribble_incomplete, md_total_cross_complete, md_total_cross_incomplete, md_total_fouls_committed, \
               md_total_fouls_won, \
               total_avg_match_pl, total_avg_shots, total_avg_total_shots_on_target, total_avg_goals, \
               total_avg_assists, total_avg_yellow_card, total_avg_red_card, total_avg_passes, \
               total_avg_passes_inc, total_avg_dribble_complete, total_avg_dribble_incomplete, total_avg_cross_complete, \
               total_avg_cross_incomplete, total_avg_fouls_committed, total_avg_fouls_won

def allForwardStats():
    teams = teamList()
    all_fw = []
    for team in teams:
        name_file = 'players/' + team + '.json'
        forwards_list = ["Forward", "Wing", "Striker"]
        with open(name_file, encoding='utf-8') as m:
            players = json.load(m)
            for player in players:
                positions = player.get('positions')
                for position in positions:
                    for word in forwards_list:
                        if re.search(word, position):
                            single_fw = player
                            single_fw['team_name'] = team
                            single_fw.pop('goalkeeper')
                            single_fw.pop('list_id_match')
                            single_fw.pop('img_web')
                            count_matches = single_fw.get('match_played')
                            single_fw['total_shots'] = round(single_fw.get('total_shots') / count_matches, 2)
                            single_fw['total_shots_on_target_pl'] = round(single_fw.get('total_shots_on_target_pl') / count_matches, 2)
                            single_fw['total_goals_pl'] = round(single_fw.get('total_goals_pl') / count_matches, 2)
                            single_fw['total_assists_pl'] = round(single_fw.get('total_assists_pl') / count_matches, 2)
                            single_fw['total_yellow_card_pl'] = round(single_fw.get('total_yellow_card_pl') / count_matches, 2)
                            single_fw['total_red_card_pl'] = round(single_fw.get('total_red_card_pl') / count_matches, 2)
                            single_fw['total_passes_pl'] = round(single_fw.get('total_passes_pl') / count_matches, 2)
                            single_fw['total_passes_inc_pl'] = round(single_fw.get('total_passes_inc_pl') / count_matches, 2)
                            single_fw['total_dribble_complete_pl'] = round(single_fw.get('total_dribble_complete_pl') / count_matches, 2)
                            single_fw['total_dribble_incomplete_pl'] = round(single_fw.get('total_dribble_incomplete_pl') / count_matches, 2)
                            single_fw['total_cross_complete_pl'] = round(single_fw.get('total_cross_complete_pl') / count_matches, 2)
                            single_fw['total_cross_incomplete_pl'] = round(single_fw.get('total_cross_incomplete_pl') / count_matches, 2)
                            single_fw['total_interc_won_pl'] = round(single_fw.get('total_interc_won_pl') / count_matches, 2)
                            single_fw['total_interc_lose_pl'] = round(single_fw.get('total_interc_lose_pl') / count_matches, 2)
                            single_fw['total_blocks_pl'] = round(single_fw.get('total_blocks_pl') / count_matches, 2)
                            single_fw['total_fouls_committed_pl'] = round(single_fw.get('total_fouls_committed_pl') / count_matches, 2)
                            single_fw['total_fouls_won_pl'] = round(single_fw.get('total_fouls_won_pl') / count_matches, 2)

                            all_fw.append(single_fw.copy())
                            break
                    else:
                        continue
                    break
    for fw in all_fw:
        print(fw)
    name_file = 'all_fw.json'
    with open(name_file, 'w', encoding='utf-8') as outfile:
        try:
            json.dump(all_fw, outfile, ensure_ascii=False, indent=4)
            print('Archivo ' + name_file + ' creado')
        except:
            print('Ocurrio un error')

def graph_spider_fw(id_player):
    with open('all_fw.json', 'r', encoding='utf-8') as m:
        all_fws = json.load(m)
        cant_fws = len(all_fws)
        total_avg_match_pl = total_avg_shots = total_avg_total_shots_on_target = total_avg_goals = \
        total_avg_assists = total_avg_yellow_card = total_avg_red_card = total_avg_passes = \
        total_avg_passes_inc = total_avg_dribble_complete = total_avg_dribble_incomplete = total_avg_cross_complete = \
        total_avg_cross_incomplete = total_avg_interc_won = total_avg_interc_lose = \
        total_avg_blocks = total_avg_fouls_committed = total_avg_fouls_won = 0

        for fw in all_fws:
            total_avg_match_pl = total_avg_match_pl + fw.get('match_played')
            total_avg_shots = total_avg_shots + fw.get('total_shots')
            total_avg_total_shots_on_target = total_avg_total_shots_on_target + fw.get('total_shots_on_target_pl')
            total_avg_goals = total_avg_goals + fw.get('total_goals_pl')
            total_avg_assists = total_avg_assists + fw.get('total_assists_pl')
            total_avg_yellow_card = total_avg_yellow_card + fw.get('total_yellow_card_pl')
            total_avg_red_card = total_avg_red_card + fw.get('total_red_card_pl')
            total_avg_passes = total_avg_passes + fw.get('total_passes_pl')
            total_avg_passes_inc = total_avg_passes_inc + fw.get('total_passes_inc_pl')
            total_avg_dribble_complete = total_avg_dribble_complete + fw.get('total_dribble_complete_pl')
            total_avg_dribble_incomplete = total_avg_dribble_incomplete + fw.get('total_dribble_incomplete_pl')
            total_avg_cross_complete = total_avg_cross_complete + fw.get('total_cross_complete_pl')
            total_avg_cross_incomplete = total_avg_cross_incomplete + fw.get('total_cross_incomplete_pl')
            total_avg_interc_won = total_avg_interc_won + fw.get('total_interc_won_pl')
            total_avg_interc_lose = total_avg_interc_lose + fw.get('total_interc_lose_pl')
            total_avg_blocks = total_avg_blocks + fw.get('total_blocks_pl')
            total_avg_fouls_committed = total_avg_fouls_committed + fw.get('total_fouls_committed_pl')
            total_avg_fouls_won = total_avg_fouls_won + fw.get('total_fouls_won_pl')

            if id_player == fw.get('player_id'):
                if fw.get('player_nickname'):
                    name_player = fw.get('player_nickname')
                else:
                    name_player = fw.get('player_name')
                fw_matches_pl = fw.get('match_played')
                fw_total_shots = fw.get('total_shots')
                fw_total_shots_on_target = fw.get('total_shots_on_target_pl')
                fw_total_goals = fw.get('total_goals_pl')
                fw_total_assists = fw.get('total_assists_pl')
                fw_total_yellow_card = fw.get('total_yellow_card_pl')
                fw_total_red_card = fw.get('total_red_card_pl')
                fw_total_passes = fw.get('total_passes_pl')
                fw_total_passes_inc = fw.get('total_passes_inc_pl')
                fw_total_dribble_complete = fw.get('total_dribble_complete_pl')
                fw_total_dribble_incomplete = fw.get('total_dribble_incomplete_pl')
                fw_total_cross_complete = fw.get('total_cross_complete_pl')
                fw_total_cross_incomplete = fw.get('total_cross_incomplete_pl')
                fw_total_fouls_committed = fw.get('total_fouls_committed_pl')
                fw_total_fouls_won = fw.get('total_fouls_won_pl')
        total_avg_match_pl = round(total_avg_match_pl / cant_fws, 2)
        total_avg_shots = round(total_avg_shots / cant_fws, 2)
        total_avg_total_shots_on_target = round(total_avg_total_shots_on_target / cant_fws, 2)
        total_avg_goals = round(total_avg_goals / cant_fws, 2)
        total_avg_assists = round(total_avg_assists / cant_fws, 2)
        total_avg_yellow_card = round(total_avg_yellow_card / cant_fws, 2)
        total_avg_red_card = round(total_avg_red_card / cant_fws, 2)
        total_avg_passes = round(total_avg_passes / cant_fws, 2)
        total_avg_passes_inc = round(total_avg_passes_inc / cant_fws, 2)
        total_avg_dribble_complete = round(total_avg_dribble_complete / cant_fws, 2)
        total_avg_dribble_incomplete = round(total_avg_dribble_incomplete / cant_fws, 2)
        total_avg_cross_complete = round(total_avg_cross_complete / cant_fws, 2)
        total_avg_cross_incomplete = round(total_avg_cross_incomplete / cant_fws, 2)
        total_avg_fouls_committed = round(total_avg_fouls_committed / cant_fws, 2)
        total_avg_fouls_won = round(total_avg_fouls_won / cant_fws, 2)

        return name_player, fw_matches_pl, fw_total_shots, fw_total_shots_on_target, fw_total_goals, fw_total_assists, \
               fw_total_yellow_card, fw_total_red_card, fw_total_passes, fw_total_passes_inc, fw_total_dribble_complete, \
               fw_total_dribble_incomplete, fw_total_cross_complete, fw_total_cross_incomplete, fw_total_fouls_committed, \
               fw_total_fouls_won, \
               total_avg_match_pl, total_avg_shots, total_avg_total_shots_on_target, total_avg_goals, \
               total_avg_assists, total_avg_yellow_card, total_avg_red_card, total_avg_passes, \
               total_avg_passes_inc, total_avg_dribble_complete, total_avg_dribble_incomplete, total_avg_cross_complete, \
               total_avg_cross_incomplete, total_avg_fouls_committed, total_avg_fouls_won

def allPlayers():
    # Save a json file with every player and his stats
    teams = teamList()
    all_pl = []
    for team in teams:
        name_file = 'players/' + team + '.json'
        with open(name_file, encoding='utf-8') as m:
            players = json.load(m)
            for player in players:
                if player.get('goalkeeper') == 'no':
                    stats = ['total_shots', 'total_shots_on_target_pl', 'total_passes_pl', 'total_passes_inc_pl',
                            'total_dribble_complete_pl', 'total_dribble_incomplete_pl', 'total_cross_complete_pl',
                            'total_cross_incomplete_pl', 'total_interc_won_pl', 'total_interc_lose_pl', 'total_blocks_pl',
                            'total_fouls_committed_pl', 'total_fouls_won_pl']
                    count_matches = player.get('match_played')
                    for stat in stats:
                        player[stat] = round(player[stat] / count_matches, 2)

                    player['team_name'] = team
                    player.pop('goalkeeper')
                    player.pop('list_id_match')
                    player.pop('img_web')
                    all_pl.append(player.copy())
    name_file = 'all_pl.json'
    with open(name_file, 'w', encoding='utf-8') as outfile:
        try:
            json.dump(all_pl, outfile, ensure_ascii=False, indent=4)
            print('Archivo ' + name_file + ' creado')
        except:
            print('Ocurrio un error')

if __name__ == "__main__":
    # allPlayers()
    # allPlayersDetails()
    # print(getImage('Messi'))
    allGoalKeepersStats()
    # allDefendersStats()
    # allMidfieldStats()
    # allForwardStats()
    # allPlayers()