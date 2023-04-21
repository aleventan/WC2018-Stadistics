from pygal.config import BaseConfig

from game_def import openJsonMatches, getIdMatch, teamList
from player_def import graph_all_gk, graph_spider_def, graph_spider_mid, graph_spider_fw
import matplotlib
matplotlib.use('Agg')
# Importing the airium library
from airium import Airium
import json
import pygal
from pygal.style import Style
import re


def gen_HTML_players(selected_team):
    #from tasks import refreshed_google_client
    a = Airium()
    # Generating HTML file
    a('<!DOCTYPE html>')
    with a.html(lang="pl"):
        with a.head():
            a.meta(charset="UTF-8")
            a.meta(content='text/html; charset=UTF-8', **{'http-equiv': 'content-type'})
            a.title(_t="Players stats for " + selected_team + " in World Cup 2018")
            a.link(href="{{ url_for(\'static\',filename=\'styles/style.css\') }}", rel='stylesheet')
            a.link(href="{{ url_for(\'static\',filename=\'js/js.js\') }}", type='text/javascript')
            a.script(src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js")
        with a.body():
            with a.div(klass='blackline'):
                lt = teamList()
                with a.p():
                    with a.div(klass='p_combo1'):
                        with a.form(method="post", action='/'):
                            with a.select(name="combo_team", klass="combo1"):
                                with a.option(selected=True):
                                    a("Choose a team")
                                for l in lt:
                                    with a.option(value=l):
                                        a(l)
                            a.input(type="submit", value="Send")
                with a.div(klass='topnav'):
                    with a.a(href="{{ url_for('match_stats') }}"):
                        a("Match Stats")
                    with a.a(href="{{ url_for('team_stats2') }}"):
                        a("Team Stats")
                    with a.a(klass="active"):
                        a("Players Stats")
            a('<br><br><br>')

            with a.div():
                name_file = 'players/' + selected_team + '.json'
                with open(name_file, 'r', encoding='utf-8', errors='ignore') as m:
                    players = json.load(m)
                    with a.div():
                        with a.select(name="combo-players", klass="combo2", id='Combo-players'):
                            with a.option(selected=True):
                                a("Choose a Player")
                            for player in players:
                                with a.option(value=player.get('player_id')):
                                    name_player = player.get('player_nickname') or player.get('player_name')
                                    a(name_player)
                    a('<br><br><br>')
                with a.div(klass='iframe_player'):
                    for player in players:
                        id_player = player.get('player_id')
                        name_player = player.get('player_nickname') or player.get('player_name')

                        with a.div(klass="stats_player", id=id_player):
                            with a.div(klass='header_player_stats'):
                                with a.div(klass='image_player'):
                                    image_player = player.get('img_web')
                                    a.img(src=image_player, alt=name_player)
                                with a.div(klass='data_player'):
                                    with a.div(klass='name_player_stats'):
                                        a("Player Name: " + name_player)
                                    with a.div(klass='position_player'):
                                        list_positions = player.get('positions')
                                        full_list_pos = ', '.join(list_positions)
                                        a('Positions: ' + full_list_pos)
                                    with a.div(klass='min_played'):
                                        min_played = player.get('total_time')
                                        count_match = player.get('match_played')
                                        a("Total Minutes Played: " + str(min_played) + " (" + str(count_match) + " matches)")
                            with a.div(klass='left_graph_player_stats'):
                                # If not goalkeeper, add other statistics
                                if any("Goalkeeper" in word for word in list_positions):
                                    pass
                                else:
                                    with a.div(klass='md_graph_goals_cards'):
                                        a('Total Goals: ' + str(player.get('total_goals_pl')))
                                        a('<br><br>')
                                        a('Total Assists: ' + str(player.get('total_assists_pl')))
                                        a('<br><br>')
                                        a('Total Yellow Cards: ' + str(player.get('total_yellow_card_pl')))
                                        a('<br><br>')
                                        a('Total Red Cards: ' + str(player.get('total_red_card_pl')))
                                forwards_list = ["Forward", "Wing", "Striker"]
                                if min_played < 90:
                                    a('He didn\'t play more than 90 minutes')
                                else:
                                    # If not goalkeeper, made a menu for the position
                                    if any("Goalkeeper" in position for position in list_positions):
                                        pass
                                    else:

                                        with a.select(name="cbo-positions", klass="combo3", id='Combo-positions'):
                                            with a.option(selected=True):
                                                a("Positions")
                                            if any("Back" in position for position in list_positions):
                                                with a.option(value='df_left'):
                                                    a('Defender')
                                            if any("Midfield" in position for position in list_positions):
                                                with a.option(value='md_left'):
                                                    a('Midfield')
                                            for position in list_positions:
                                                for word in forwards_list:
                                                    if re.search(word, position):
                                                        with a.option(value='fw_left'):
                                                            a('Forward')
                                                            break
                                                else:
                                                    continue
                                                break
                                    # Gk left graph
                                    with a.div(klass='gk_left', id='gk_left'):
                                        if any("Goalkeeper" in word for word in list_positions):
                                            with a.div(klass='clean_sheets_gk'):
                                                a('Clean Sheets: ' + str(player.get('total_clean_sheets')))
                                            with a.div(klass='total_goals_conceded_gk'):
                                                a('Total Goals Conceded: ' + str(player.get('total_goals_conceded_gk')))
                                            with a.div(klass='total_shots_saved_gk'):
                                                a('Total Shots Saved: ' + str(player.get('total_shots_saved_gk')))
                                            with a.div(klass='graph_gk_alone'):
                                                custom_style = Style(background='transparent', legend_hover=False,
                                                                     plot_background='transparent', colors=('DarkBlue', 'OrangeRed'))
                                                line_chart = pygal.StackedBar(legend_at_bottom=True, style=custom_style)
                                                line_chart.title = 'Goalkeeper stats per 90\''
                                                line_chart.x_labels = [name_player]
                                                shots_saved_gk = round(player.get('total_shots_saved_gk') / count_match, 2)
                                                goal_conceded_gk = round(player.get('total_goals_conceded_gk') / count_match, 2)
                                                line_chart.add('Total Shots Saved per 90\'', shots_saved_gk)
                                                line_chart.add('Total Goals Conceded per 90\'', goal_conceded_gk)
                                                show_line = line_chart.render_data_uri()
                                                a.embed(type="image/svg+xml", src=show_line, style="width:95%")
                                    # df left graph
                                    with a.div(klass='df_left', id='df_left'):
                                        if any("Back" in word for word in list_positions):
                                            for_graph_all_dfs = graph_spider_def(id_player)
                                            custom_style = Style(background='transparent', legend_hover=False,
                                                                 plot_background='transparent', colors=('Blue', 'Green'))
                                            radar_chart = pygal.Radar(legend_at_bottom=True, style=custom_style)
                                            radar_chart.title = name_player + ' stats vs. Rest of Defenders of the Tournament (per 90\')'
                                            radar_chart.x_labels = ['Avg. Crosses Completed',
                                                                    'Avg. Crosses Incomplete', 'Avg. Interception Won', 'Avg. Interception Lose',
                                                                    'Avg. Blocks', 'Avg. Fouls Committed']
                                            radar_chart.add(name_player, [for_graph_all_dfs[6], for_graph_all_dfs[7],
                                                                          for_graph_all_dfs[8], for_graph_all_dfs[9],for_graph_all_dfs[10],
                                                                          for_graph_all_dfs[11]])
                                            radar_chart.add('Rest of Defenders', [for_graph_all_dfs[17], for_graph_all_dfs[18],
                                                                                  for_graph_all_dfs[19], for_graph_all_dfs[20], for_graph_all_dfs[21],
                                                                                  for_graph_all_dfs[22]])
                                            show_radar = radar_chart.render_data_uri()
                                            a.embed(type="image/svg+xml", src=show_radar)
                                    # md left graph
                                    with a.div(klass='md_left', id='md_left'):
                                        if any("Midfield" in word for word in list_positions):
                                            # First made a combo for stats and passes
                                            with a.select(name="cbo-stats_left", klass="combo4", id='Combo-stats-left'):
                                                with a.option(selected=True):
                                                    a("Stats")
                                                with a.option(value='md_graph_most'):
                                                    a('In-Game Stats')
                                                with a.option(value='md_graph_pass'):
                                                    a('Passes')
                                            # The graph with stats
                                            with a.div(klass='md_graph_most'):
                                                for_graph_all_mds = graph_spider_mid(id_player)
                                                custom_style = Style(background='transparent', legend_hover=False,
                                                                     plot_background='transparent', colors=('Blue', 'Green'))
                                                radar_chart = pygal.Radar(legend_at_bottom=True, style=custom_style)
                                                radar_chart.title = name_player + ' stats vs. Rest of Midfields of the Tournament (per 90\')'
                                                radar_chart.x_labels = ['Avg. Shots', 'Avg. Shots on Target', 'Avg. Dribbles Completed',
                                                                        'Avg. Dribbles Incomplete', 'Avg. Fouls Committed', 'Avg. Fouls Won']
                                                radar_chart.add(name_player, [for_graph_all_mds[2], for_graph_all_mds[3], for_graph_all_mds[10],
                                                                              for_graph_all_mds[11], for_graph_all_mds[14], for_graph_all_mds[15]])
                                                radar_chart.add('Rest of Midfields', [for_graph_all_mds[17], for_graph_all_mds[18], for_graph_all_mds[25],
                                                                                      for_graph_all_mds[26], for_graph_all_mds[29], for_graph_all_mds[30]])
                                                show_radar = radar_chart.render_data_uri()
                                                a.embed(type="image/svg+xml", src=show_radar)
                                            # The graph with passes
                                            with a.div(klass='md_graph_pass'):
                                                for_graph_all_mds = graph_spider_mid(id_player)
                                                custom_style = Style(background='transparent', legend_hover=False,
                                                                     plot_background='transparent', colors=('Blue', 'Green'))
                                                bar_chart = pygal.StackedBar(print_values=True, legend_at_bottom=True, style=custom_style)
                                                bar_chart.title = radar_chart.title
                                                bar_chart.x_labels = [name_player, 'Rest of Midfield (per 90\')']
                                                passes_comp_md = round(for_graph_all_mds[8] / (for_graph_all_mds[8] + for_graph_all_mds[9]) * 100)
                                                passes_incomp_md = round(for_graph_all_mds[9] / (for_graph_all_mds[8] + for_graph_all_mds[9]) * 100)
                                                passes_comp_rest = round(for_graph_all_mds[23] / (for_graph_all_mds[23] + for_graph_all_mds[24]) * 100)
                                                passes_incomp_rest = round(for_graph_all_mds[24] / (for_graph_all_mds[23] + for_graph_all_mds[24]) * 100)
                                                bar_chart.add('Avg. Passes Completed per 90', [{'value': passes_comp_md, 'label': str(for_graph_all_mds[8]) + ' avg. per 90\''},
                                                                                               {'value': passes_comp_rest, 'label': str(for_graph_all_mds[23]) + ' avg. per 90\''}])
                                                bar_chart.add('Avg. Passes Incomplete per 90', [{'value': passes_incomp_md, 'label': str(for_graph_all_mds[9]) + ' avg. per 90\''},
                                                                                               {'value': passes_incomp_rest, 'label': str(for_graph_all_mds[24]) + ' avg. per 90\''}])
                                                bar_chart.value_formatter = lambda x:  '%s%%' % x
                                                show_line = bar_chart.render_data_uri()
                                                a.embed(type="image/svg+xml", src=show_line)
                                    # fw left graph
                                    with a.div(klass='fw_left', id='fw_left'):
                                        # Search if any of the words from forwards_list are in the list_positions
                                        for position in list_positions:
                                            for word in forwards_list:
                                                if re.search(word, position):
                                                    # First made a combo for stats and passes
                                                    with a.select(name="cbo-stats_left", klass="combo4", id='Combo-stats-left'):
                                                        with a.option(selected=True):
                                                            a("Stats")
                                                        with a.option(value='fw_graph_most'):
                                                            a('In-Game Stats')
                                                        with a.option(value='fw_graph_pass'):
                                                            a('Passes')
                                                    # The graph with stats
                                                    with a.div(klass='fw_graph_most'):
                                                        for_graph_all_fws = graph_spider_fw(id_player)
                                                        custom_style = Style(background='transparent', legend_hover=False,
                                                                             plot_background='transparent', colors=('Blue', 'Green'))
                                                        radar_chart = pygal.Radar(legend_at_bottom=True, style=custom_style)
                                                        radar_chart.title = name_player + ' stats vs. Rest of Forwards of the Tournament (per 90\')'
                                                        radar_chart.x_labels = ['Avg. Shots', 'Avg. Shots on Target', 'Avg. Dribbles Completed', 'Avg. Dribbles Incomplete',
                                                                                'Avg. Crosses Completed', 'Avg. Crosses Incomplete', 'Avg. Fouls Won']
                                                        radar_chart.add(name_player, [for_graph_all_fws[2], for_graph_all_fws[3], for_graph_all_fws[10],
                                                                                      for_graph_all_fws[11], for_graph_all_fws[12], for_graph_all_fws[13],
                                                                                      for_graph_all_fws[15]])
                                                        radar_chart.add('Rest of Forwards', [for_graph_all_fws[17], for_graph_all_fws[18], for_graph_all_fws[25],
                                                                                              for_graph_all_fws[26], for_graph_all_fws[27], for_graph_all_fws[28],
                                                                                              for_graph_all_fws[30]])
                                                        show_radar = radar_chart.render_data_uri()
                                                        a.embed(type="image/svg+xml", src=show_radar)
                                                    # The graph with passes
                                                    with a.div(klass='fw_graph_pass'):
                                                        for_graph_all_fws = graph_spider_fw(id_player)
                                                        custom_style = Style(background='transparent', legend_hover=False,
                                                                             plot_background='transparent', colors=('Blue', 'Green'))
                                                        bar_chart = pygal.StackedBar(print_values=True, legend_at_bottom=True, style=custom_style)
                                                        bar_chart.title = radar_chart.title
                                                        bar_chart.x_labels = [name_player, 'Rest of Midfield (per 90\')']
                                                        passes_comp_fw = round(for_graph_all_fws[8] / (for_graph_all_fws[8] + for_graph_all_fws[9]) * 100)
                                                        passes_incomp_fw = round(for_graph_all_fws[9] / (for_graph_all_fws[8] + for_graph_all_fws[9]) * 100)
                                                        passes_comp_rest = round(for_graph_all_fws[23] / (for_graph_all_fws[23] + for_graph_all_fws[24]) * 100)
                                                        passes_incomp_rest = round(for_graph_all_fws[24] / (for_graph_all_fws[23] + for_graph_all_fws[24]) * 100)
                                                        bar_chart.add('Avg. Passes Completed per 90', [{'value': passes_comp_fw, 'label': str(for_graph_all_fws[8]) + ' avg. per 90\''},
                                                                                                       {'value': passes_comp_rest, 'label': str(for_graph_all_fws[23]) + ' avg. per 90\''}])
                                                        bar_chart.add('Avg. Passes Incomplete per 90', [{'value': passes_incomp_fw, 'label': str(for_graph_all_fws[9]) + ' avg. per 90\''},
                                                                                                       {'value': passes_incomp_rest, 'label': str(for_graph_all_fws[24]) + ' avg. per 90\''}])
                                                        bar_chart.value_formatter = lambda x:  '%s%%' % x
                                                        show_line = bar_chart.render_data_uri()
                                                        a.embed(type="image/svg+xml", src=show_line)
                                                    break
                                            else:
                                                continue
                                            break
                            # Right graphs
                            with a.div(klass='right_graph_player_stats'):
                                # If is goalkeeper made a graph, if not take the 20 best from different statistics
                                if list_positions[0] == 'Goalkeeper':
                                    # devuelve una tupla. se accede por indice
                                    for_graph_all_gks = graph_all_gk(id_player)
                                    custom_style = Style(background='transparent', legend_hover=False,
                                                         plot_background='transparent', colors=('Blue', 'Green'))
                                    radar_chart = pygal.Radar(legend_at_bottom=True, style=custom_style)
                                    radar_chart.title = 'Goalkeeper stats vs. Rest of Goalkeepers of the Tournament (per 90\')'
                                    radar_chart.x_labels = ['Total Matches', 'Passes Incompleted', 'Shots Saved',
                                                            'Total Goals Conceded', 'Total Clean Sheets']
                                    radar_chart.add(name_player, [for_graph_all_gks[1], for_graph_all_gks[3], for_graph_all_gks[6],
                                                                  for_graph_all_gks[7], for_graph_all_gks[9]])
                                    radar_chart.add('Rest of Goalkeepers', [for_graph_all_gks[10], for_graph_all_gks[12], for_graph_all_gks[15],
                                                                            for_graph_all_gks[16], for_graph_all_gks[18]])
                                    show_radar = radar_chart.render_data_uri()
                                    a.embed(type="image/svg+xml", src=show_radar, style="width:95%")
                                else:
                                    dict_list_elements = dict()
                                    dict_list_elements['total_shots'] = 'Total Shots (avg. per 90\')'
                                    dict_list_elements['total_shots_on_target_pl'] = 'Total Shots on Target (avg. per 90\')'
                                    dict_list_elements['total_goals_pl'] = 'Total Goals Scored'
                                    dict_list_elements['total_assists_pl'] = 'Total Assists'
                                    dict_list_elements['total_passes_pl'] = 'Total Passes Completed (avg. per 90\')'
                                    dict_list_elements['total_dribble_complete_pl'] = 'Total Dribbles Completed (avg. per 90\')'
                                    dict_list_elements['total_cross_complete_pl'] = 'Total Crosses Completed (avg. per 90\')'
                                    dict_list_elements['total_interc_won_pl'] = 'Total Interceptions Won (avg. per 90\')'
                                    dict_list_elements['total_blocks_pl'] = 'Total Blocks Won (avg. per 90\')'
                                    dict_list_elements['total_fouls_won_pl'] = 'Total Fouls Won (avg. per 90\')'
                                    list_cbo = []
                                    for clave, valor in dict_list_elements.items():
                                        file_name_json = clave + '_top20.json'
                                        with open(file_name_json, encoding='utf-8') as m:
                                            players_all = json.load(m)
                                            for pl_graph in players_all:
                                                if pl_graph.get('player_nickname'):
                                                    name_player_graph = pl_graph.get('player_nickname')
                                                else:
                                                    name_player_graph = pl_graph.get('player_name')
                                                if name_player_graph == name_player:
                                                    type_graph = {clave: valor}
                                                    list_cbo.append(type_graph)

                                    if list_cbo:
                                        with a.select(name="combo_graph_all_pl", klass="combo_graph_all_pl", id="combo-graph-all-pl"):
                                            with a.option(selected=True):
                                                a("Choose a Stat")
                                            for type_gp in list_cbo:
                                                for clave_cb, valor_cb in type_gp.items():
                                                    with a.option(value=clave_cb):
                                                        a(valor_cb)
                                        with a.div(klass='graph_all_right'):
                                            for type_gp in list_cbo:
                                                for clave_gp, valor_gp in type_gp.items():
                                                    with a.div(klass=clave_gp, id=clave_gp):
                                                        custom_style = Style(background='transparent', plot_background='transparent',
                                                                             legend_font_size=12, value_colors='Black')
                                                        bar_chart = pygal.Bar(print_values=True,
                                                                              style=custom_style, legend_at_bottom=True, spacing=1,
                                                                              print_values_position='top')
                                                        file_name_json = clave_gp + '_top20.json'
                                                        with open(file_name_json, encoding='utf-8') as m:
                                                            players_all = json.load(m)
                                                            for pl_graph in players_all:
                                                                if pl_graph.get('player_nickname'):
                                                                    name_player_on_graph = pl_graph.get('player_nickname')
                                                                else:
                                                                    name_player_on_graph = pl_graph.get('player_name')
                                                                if name_player_on_graph == name_player:
                                                                    name_player_and_nation = name_player_on_graph + '(' + pl_graph.get('team_name')[:3] + '.)'
                                                                    bar_chart.add(name_player_and_nation, [{'value': pl_graph.get(clave_gp),
                                                                                                          'style': 'opacity:10;stroke: black; stroke-width: 9'}])
                                                                else:
                                                                    name_player_and_nation = name_player_on_graph + '(' + pl_graph.get('team_name')[:3] + '.)'
                                                                    bar_chart.add(name_player_and_nation, [{'value': pl_graph.get(clave_gp),
                                                                                                          'style': 'opacity: 0.2; stroke: black; stroke-width: 4'}])
                                                        show_bar = bar_chart.render_data_uri()
                                                        a.embed(type="image/svg+xml", src=show_bar)
                                    else:
                                        with a.div(klass='no_stats_right'):
                                            a(name_player + ' isn\'t listed in the top 20 of any statistical categories')
                # Made javascript / Jquery for hide and show menues and divs
                with a.script(type="text/javascript"):
                    s = '''$(document).ready(function () {
        $('.stats_player').hide();
        $('.total_shots').hide();
        $('.total_shots_on_target_pl').hide();
        $('.total_goals_pl').hide();
        $('.total_assists_pl').hide();
        $('.total_passes_pl').hide();
        $('.total_dribble_complete_pl').hide();
        $('.total_cross_complete_pl').hide();
        $('.total_interc_won_pl').hide();
        $('.total_blocks_pl').hide();
        $('.total_fouls_won_pl').hide();
        
        $(".df_left").hide();
        $(".md_left").hide();
        $(".fw_left").hide();
        $(".md_graph_most").hide();
        $(".md_graph_pass").hide();
        $(".fw_graph_most").hide();
        $(".fw_graph_pass").hide();
        
        $('body').on('change', '#Combo-positions', function() {
            var valorSeleccionado = $(this).val();
            
            $(".df_left").hide();
            $(".md_left").hide();
            $(".fw_left").hide();
            $(".md_graph_most").hide();
            $(".md_graph_pass").hide();
            $(".fw_graph_most").hide();
            $(".fw_graph_pass").hide();
            

            if (valorSeleccionado == "gk_left") {
               $(".gk_left").show();
            } else if (valorSeleccionado == "df_left") {
               $(".df_left").show();
            } else if (valorSeleccionado == "md_left") {
               $(".md_left").show();
            } else if (valorSeleccionado == "fw_left") {
               $(".fw_left").show();
            }
            
            $("#Combo-stats-left").prop("selectedIndex",0);
        });
        
        $('body').on('change', '#Combo-stats-left', function() {
            var valorSeleccionado2 = $(this).val();
            $(".md_graph_most").hide();
            $(".md_graph_pass").hide();
            $(".fw_graph_most").hide();
            $(".fw_graph_pass").hide();
            
            if (valorSeleccionado2 == 'md_graph_most'){
                $(".md_graph_most").show();
            } else if (valorSeleccionado2 == 'md_graph_pass'){
                $(".md_graph_pass").show();
            } else if (valorSeleccionado2 == 'fw_graph_most'){
                $(".fw_graph_most").show();
            } else if (valorSeleccionado2 == 'fw_graph_pass'){
                $(".fw_graph_pass").show();
            }
        });
        
        $('body').on('change', '#Combo-players', function() {
            $('.stats_player').hide();
            
            $(".df_left").hide();
            $(".md_left").hide();
            $(".fw_left").hide();
            $('#'+$(this).val()).show();
        });
        
        $('body').on('change', '#combo-graph-all-pl', function() {
            $('.total_shots').hide();
            $('.total_shots_on_target_pl').hide();
            $('.total_goals_pl').hide();
            $('.total_assists_pl').hide();
            $('.total_passes_pl').hide();
            $('.total_dribble_complete_pl').hide();
            $('.total_cross_complete_pl').hide();
            $('.total_interc_won_pl').hide();
            $('.total_blocks_pl').hide();
            $('.total_fouls_won_pl').hide();
            $('.'+$(this).val()).show();
        });
        
        });'''
                    a(s)

    # Casting the file to a string to extract the value
    html = str(a)
    # Casting the file to UTF-8 encoded bytes:
    html_bytes = bytes(a)
    # print(type(html))
    h = open('templates/players_stats.html', 'w', encoding='UTF-8')
    h.write(html)

    # close the file
    h.close()


if __name__ == "__main__":
    gen_HTML_players("Argentina")
    # survey({'Prueba': [19,10]}, ['Argentina', 'Chile'])
    # plt.show()