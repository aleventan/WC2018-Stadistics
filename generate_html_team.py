import pygal
from pygal.config import BaseConfig
from pygal.style import Style, CleanStyle
from game_def import openJsonMatches, getIdMatch, teamList
import json
import matplotlib
matplotlib.use('Agg')
# Importing the airium library
from airium import Airium
from operator import itemgetter


def gen_HTML(selected_team):
    #from tasks import refreshed_google_client
    a = Airium()
    # Generating HTML file
    a('<!DOCTYPE html>')
    with a.html(lang="pl"):
        with a.head():
            a.meta(charset="utf-8")
            a.title(_t="Team stats for " + selected_team + " in World Cup 2018")
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
                                    # if lt.index(l) % 4:
                                    #     with a.optgroup():
                                    #         a("Group A")
                                    with a.option(value=l):
                                        a(l)
                            a.input(type="submit", value="Send")
                with a.div(klass='topnav'):
                    with a.a(href="{{ url_for('match_stats') }}"):
                        a("Match Stats")
                    with a.a(klass="active"):
                        a("Team Stats")
                    with a.a(href="{{ url_for('players_stats') }}"):
                        a("Players Stats")
            a('<br><br><br>')
            a('<br><br><br>')

            with a.div(klass='div_team_complete'):
                # Open the json with all the data from the teams
                with open('total_stats.json', 'r') as total_team_json:
                    data = json.load(total_team_json)
                    for i in data:
                        if i.get('selected_team') == selected_team:
                            # Made a table with statistics about the selected team
                            with a.table(klass='table_team_stats'):
                                with a.tr():
                                    with a.td():
                                        flag_team_name = "{{ url_for(\'static\',filename=\'./flags/\') }}" + selected_team + ".png"
                                        a.img(src=flag_team_name, alt=selected_team, klass="flags", align="left")
                                    with a.td():
                                        a(selected_team)
                                with a.tr(klass='row_table_team'):
                                    with a.td(klass='column_table_team'):
                                        a('Stage Reached: ')
                                    with a.td(klass='column_table_team'):
                                        a(i.get('stage_reached'))
                                with a.tr(klass='row_table_team'):
                                    with a.td(klass='column_table_team'):
                                        a('Average Goal p/Game: ')
                                    with a.td(klass='column_table_team'):
                                        a(i.get('avg_goals_scored'))
                                with a.tr(klass='row_table_team'):
                                    with a.td(klass='column_table_team'):
                                        a('Goals Scored: ')
                                    with a.td(klass='column_table_team'):
                                        a(i.get('count_total_goals_scored'))
                                with a.tr(klass='row_table_team'):
                                    with a.td(klass='column_table_team'):
                                        a('Goals Conceded: ')
                                    with a.td(klass='column_table_team'):
                                        a(i.get('count_total_goals_conceded'))
                                with a.tr(klass='row_table_team'):
                                    with a.td(klass='column_table_team'):
                                        a('Goal Difference: ')
                                    with a.td(klass='column_table_team'):
                                        a(i.get('goal_difference'))
                                with a.tr(klass='row_table_team'):
                                    with a.td(klass='column_table_team'):
                                        a('Shots: ')
                                    with a.td(klass='column_table_team'):
                                        a(i.get('count_total_shots'))
                                with a.tr(klass='row_table_team'):
                                    with a.td(klass='column_table_team'):
                                        a('Average Shots p/Game: ')
                                    with a.td(klass='column_table_team'):
                                        a(i.get('avg_shots'))
                                with a.tr(klass='row_table_team'):
                                    with a.td(klass='column_table_team'):
                                        a('Shots on Target: ')
                                    with a.td(klass='column_table_team'):
                                        percentage_shots = round((i.get('count_shots_on_target') / i.get('count_total_shots')) * 100)
                                        shots_on_target = str(i.get('count_shots_on_target')) + ' (' + str(percentage_shots) +'%)'
                                        a(shots_on_target)
                                with a.tr(klass='row_table_team'):
                                    with a.td(klass='column_table_team'):
                                        a('Average Shots on Target p/Game: ')
                                    with a.td(klass='column_table_team'):
                                        a(i.get('avg_shots_on_target'))
                                with a.tr(klass='row_table_team'):
                                    with a.td(klass='column_table_team'):
                                        a('Clean Sheets: ')
                                    with a.td(klass='column_table_team'):
                                        a(i.get('count_clean_sheets'))
                                with a.tr(klass='row_table_team'):
                                    with a.td(klass='column_table_team'):
                                        a('Yellow Cards: ')
                                    with a.td(klass='column_table_team'):
                                        a(i.get('count_yellow_cards'))
                                with a.tr(klass='row_table_team'):
                                    with a.td(klass='column_table_team'):
                                        a('Average Yellow Cards: ')
                                    with a.td(klass='column_table_team'):
                                        a(i.get('avg_yellow_card'))
                                with a.tr(klass='row_table_team'):
                                    with a.td(klass='column_table_team'):
                                        a('Red Cards: ')
                                    with a.td(klass='column_table_team'):
                                        a(i.get('count_red_cards'))
                                with a.tr(klass='row_table_team'):
                                    with a.td(klass='column_table_team'):
                                        a('Average red Cards: ')
                                    with a.td(klass='column_table_team'):
                                        a(i.get('avg_red_card'))

                # Made different graphs and compare the selected team with the rest
                with a.div(klass='div_graph_team'):
                    dict_graph = dict()
                    dict_graph['count_total_goals_scored'] = 'Total Goals Scored'
                    dict_graph['avg_goals_scored'] = 'Avg. Goals Scored p/game'
                    dict_graph['count_total_goals_conceded'] = 'Total Goals Conceded'
                    dict_graph['avg_goals_conceded'] = 'Avg. Goals Conceded p/game'
                    dict_graph['goal_difference'] = 'Goal Difference'
                    dict_graph['avg_shots'] = 'Avg. Shots p/game'
                    dict_graph['count_shots_on_target'] = 'Total Shots on target'
                    dict_graph['avg_shots_on_target'] = 'Avg. shots on target'
                    dict_graph['count_clean_sheets'] = 'Clean Sheets'
                    dict_graph['count_yellow_cards'] = 'Total Yellow cards'
                    dict_graph['avg_yellow_card'] = 'Avg. Yellow cards p/game'
                    dict_graph['count_red_cards'] = 'Total Red cards'
                    dict_graph['avg_red_card'] = 'Avg. Red cards p/game'
                    dict_graph['avg_poss_team'] = 'Avg. Possesion\'s team'
                    with a.select(name="combo_stats", klass="combo_stats_team", id="Combo-stats"):
                        for key, value in dict_graph.items():
                            with a.option(value=key):
                                a(value)
                    for key, value in dict_graph.items():
                        id_graph = key
                        title_graph = value
                        list_colors = []
                        list_text_colors = []
                        data.sort(key=itemgetter(id_graph), reverse=True)
                        for e in data:
                            color = e.get('color_team')
                            list_text_colors.append('Black')
                            list_colors.append(color)
                        tuple_colors = tuple(list_colors)
                        tuple_text_colors = tuple(list_text_colors)
                        custom_style = Style(
                            background='transparent', plot_background='transparent',
                            colors=tuple_colors, legend_font_size=12, value_colors=tuple_text_colors)
                        bar_chart = pygal.Bar(print_values=True,
                                              style=custom_style, width=1000, margin=0, legend_at_bottom=True, spacing=1,
                                              print_values_position='top')
                        with a.div(klass="stats", id=id_graph):
                            bar_chart.title = title_graph
                            for e in data:
                                if e.get('selected_team') == selected_team:
                                    bar_chart.add(e.get('selected_team'),[{
                                        'value': e.get(id_graph),
                                        'style': 'opacity:10;stroke: black; stroke-width: 9'}])
                                else:
                                    bar_chart.add(e.get('selected_team'), [{'value': e.get(id_graph),
                                                                            'style': 'opacity: 0.2; stroke: black; stroke-width: 4'}])
                            show_bar = bar_chart.render_data_uri()
                            a.embed(type="image/svg+xml", src=show_bar)
                    with a.script(type="text/javascript"):
                        s = '''$(document).ready(function () {
    $('.stats').hide();
    $('#count_total_goals_scored').show();
    $('body').on('change', '#Combo-stats', function() {
        $('.stats').hide();
        $('#'+$(this).val()).show();
    }); 
    });'''
                        a(s)
    # Casting the file to a string to extract the value
    html = str(a)
    # Casting the file to UTF-8 encoded bytes:
    html_bytes = bytes(a)
    print(html)
    h = open('templates/team_stats.html', 'w')
    h.write(str(html))

    # close the file
    h.close()


if __name__ == "__main__":
    gen_HTML("Egypt")
    # survey({'Prueba': [19,10]}, ['Argentina', 'Chile'])
    # plt.show()