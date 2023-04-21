from game_def import openJsonMatches, getIdMatch, teamList
import json
import pygal
from pygal.style import Style, DefaultStyle
import matplotlib
matplotlib.use('Agg')
# Importing the airium library
from airium import Airium

def gen_HTML_match(selected_team):
    #from tasks import refreshed_google_client
    a = Airium()
    # Generating HTML file
    a('<!DOCTYPE html>')
    with a.html(lang="pl"):
        with a.head():
            a.meta(charset="utf-8")
            a.title(_t="Match stats for " + selected_team + " in World Cup 2018")
            a.link(href="{{ url_for(\'static\',filename=\'styles/style.css\') }}", rel='stylesheet')
            a.link(href="{{ url_for(\'static\',filename=\'js/js.js\') }}", type='text/javascript')
        with a.body():
            with a.div(klass='blackline'):
                id_matches = getIdMatch(selected_team)
                # Arma una nueva lista con los datos de cada partido por separado
                res = list(zip(*id_matches))
                print(res)
                with open('all_matches_stats.json', 'r') as m:
                    matches = json.load(m)
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
                    with a.a(klass="active"):
                        a("Match Stats")
                    with a.a(href="{{ url_for('team_stats2') }}"):
                        a("Team Stats")
                    with a.a(href="{{ url_for('players_stats') }}"):
                        a("Players Stats")
            a('<br><br><br>')
            a('<br><br><br>')

            for match in matches:

                ht = match['home_team_name']
                at = match['away_team_name']
                hp = match['count_poss_home']
                ap = match['count_poss_away']
                if selected_team == ht or selected_team == at:
                    with a.div(klass="div_left"):
                        with a.table():
                            with a.tr():
                                with a.td(klass="result_left"):
                                    # If the match has penalties, wrote the goals count
                                    for r in res:
                                        if match['id_match'] == r[0]:
                                            if match['count_penalties_home'] > 0 and match['count_penalties_away'] > 0:
                                                a('(' + str(match['count_penalties_home']) + ')')
                                            a(r[5])
                                    flag_home_team = "{{ url_for(\'static\',filename=\'./flags/\') }}" + ht + ".png"
                                    a.img(src=flag_home_team, alt=ht, klass="flags", align="right")
                                with a.td(klass="date"):
                                    for r in res:
                                        # Separate the date
                                        if match['id_match'] == r[0]:
                                            date_m = str(r[1].split('-'))
                                            date_match = date_m[16:18] + '-' + date_m[10:12] + '-' + date_m[2:6] + '<br>'
                                            a(date_match)
                                            a(r[2])
                                with a.td():
                                    for r in res:
                                        if match['id_match'] == r[0]:
                                            a(r[6])
                                            if match['count_penalties_home'] > 0 and match['count_penalties_away'] > 0:
                                                a('(' + str(match['count_penalties_away']) + ')')
                                    flag_away_team_name = "{{ url_for(\'static\',filename=\'./flags/\') }}" + at + ".png"
                                    a.img(src=flag_away_team_name, alt=at, klass="flags", align="left")
                            with a.tr():
                                with a.th(klass="leftside"):
                                    a(ht)
                                with a.th():
                                    a("Stadistics")
                                with a.th(klass="rightside"):
                                    a(at)
                            with a.tr():
                                with a.td(klass="leftside"):
                                    a(str(hp) + '%')
                                with a.td(klass="centerside"):
                                    a("Possesion")
                                with a.td(klass="rightside"):
                                    a(str(ap) + '%')
                            with a.tr():
                                with a.td(klass="leftside"):
                                    a(match['count_shot_home'])
                                with a.td(klass="centerside"):
                                    a("Shots")
                                with a.td(klass="rightside"):
                                    a(match['count_shot_away'])
                            with a.tr():
                                with a.td(klass="leftside"):
                                    a(match['count_shots_on_target_home'])
                                with a.td(klass="centerside"):
                                    a("Shots on Target")
                                with a.td(klass="rightside"):
                                    a(match['count_shots_on_target_away'])
                            with a.tr():
                                with a.td(klass="leftside"):
                                    a(match['count_ball_recovery_home'])
                                with a.td(klass="centerside"):
                                    a("Ball Recovery")
                                with a.td(klass="rightside"):
                                    a(match['count_ball_recovery_away'])
                            with a.tr():
                                with a.td(klass="leftside"):
                                    a(match['count_fouls_committed_home'])
                                with a.td(klass="centerside"):
                                    a("Fouls Committed")
                                with a.td(klass="rightside"):
                                    a(match['count_fouls_committed_away'])
                            with a.tr():
                                with a.td(klass="leftside"):
                                    a(match['count_corner_home'])
                                with a.td(klass="centerside"):
                                    a("Corners")
                                with a.td(klass="rightside"):
                                    a(match['count_corner_away'])
                            with a.tr():
                                with a.td(klass="leftside"):
                                    a(match['count_block_home'])
                                with a.td(klass="centerside"):
                                    a("Blocks")
                                with a.td(klass="rightside"):
                                    a(match['count_block_away'])
                            with a.tr():
                                with a.td(klass="leftside"):
                                    a(match['count_interception_home'])
                                with a.td(klass="centerside"):
                                    a("Interception")
                                with a.td(klass="rightside"):
                                    a(match['count_interception_away'])

                    color_home = match['color_home']
                    color_away = match['color_away']
                    text_color_home = match['text_color_home']
                    text_color_away = match['text_color_away']

                    # Made a pie chart for the possesion
                    with a.div(klass="div_center"):
                        custom_style = Style(background='transparent', legend_hover=False,
                                             plot_background='transparent',
                                             legend_font_size=25, value_font_size=30,
                                             value_colors=(text_color_away, text_color_home),
                                             colors=(color_away, color_home))
                        pie_chart = pygal.Pie(print_values=True, legend_box_size=38, style=custom_style)
                        pie_chart.title = "Possesion"
                        pie_chart.add(at, match['count_poss_away'])
                        pie_chart.add(ht, match['count_poss_home'])
                        pie_chart.value_formatter = lambda x:  '%s%%' % x
                        show_pie = pie_chart.render_data_uri()
                        a.embed(type="image/svg+xml", src=show_pie, style="width:500px;height:400px")

                    # Made a bar chart to compare different stats
                    with a.div(klass="div_right"):
                        custom_style = Style(background='transparent', legend_hover=False,
                                             plot_background='transparent',
                                             legend_font_size=25, value_font_size=30,
                                             value_colors=(text_color_home, text_color_away),
                                             colors=(color_home, color_away))
                        bar_chart = pygal.Bar(print_values=True, style=custom_style)
                        bar_chart.x_labels = ["Shots", "Shots on Target", "Fouls", "Corners", "Blocks", "Interceptions"]
                        bar_chart.add(ht, [match['count_shot_home'], match['count_shots_on_target_home'],
                                           match['count_fouls_committed_home'], match['count_corner_home'],
                                           match['count_block_home'], match['count_interception_home']])
                        bar_chart.add(at, [match['count_shot_away'], match['count_shots_on_target_away'],
                                           match['count_fouls_committed_away'], match['count_corner_away'],
                                           match['count_block_away'], match['count_interception_away']])
                        show_pie = bar_chart.render_data_uri()
                        a.embed(type="image/svg+xml", src=show_pie, style="width:1100px;height:500px")

    # Casting the file to a string to extract the value
    html = str(a)
    # Casting the file to UTF-8 encoded bytes:
    html_bytes = bytes(a)
    print(html)
    h = open('templates/match_stats.html', 'w')
    h.write(str(html))

    # close the file
    h.close()


if __name__ == "__main__":
    gen_HTML_match("Uruguay")
    # survey({'Prueba': [19,10]}, ['Argentina', 'Chile'])
    # plt.show()