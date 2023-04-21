from flask import url_for

from game_def import teamList
import matplotlib
matplotlib.use('Agg')
from airium import Airium

def gen_HTML_index(selected_team):
    a = Airium()
    # Generating HTML file
    a('<!DOCTYPE html>')
    with a.html(lang="pl"):
        with a.head():
            a.meta(charset="utf-8")
            a.title(_t="World Cup 2018 Stadistics")
            a.link(href="{{ url_for(\'static\',filename=\'styles/style.css\') }}", rel='stylesheet')
            a.link(href="{{ url_for(\'static\',filename=\'js/js.js\') }}", type='text/javascript')
        with a.body():
            lt = teamList()
            with a.table(klass='table_flags_index'):
                # Separe the 32 teams in 4 rows
                with a.tr(klass='tr_flags_index'):
                    for l in lt[:8]:
                        with a.td(klass='td_flags_index'):
                            link_flag = url_for('team_stats', team_name=l)
                            with a.a(href=link_flag):
                                with a.p(klass='p_flags_index'):
                                    a(l)
                                flag_name = "{{ url_for(\'static\',filename=\'./flags/\') }}" + l + ".png"
                                a.img(src=flag_name, alt=l, klass="flags_index", align="left", name=l)
                with a.tr(klass='tr_flags_index'):
                    for l in lt[8:16]:
                        with a.td(klass='td_flags_index'):
                            link_flag = url_for('team_stats', team_name=l)
                            with a.a(href=link_flag):
                                with a.p(klass='p_flags_index'):
                                    a(l)
                                flag_name = "{{ url_for(\'static\',filename=\'./flags/\') }}" + l + ".png"
                                a.img(src=flag_name, alt=l, klass="flags_index", align="left", name=l)
                with a.tr(klass='tr_flags_index'):
                    for l in lt[16:24]:
                        with a.td(klass='td_flags_index'):
                            link_flag = url_for('team_stats', team_name=l)
                            with a.a(href=link_flag):
                                with a.p(klass='p_flags_index'):
                                    a(l)
                                flag_name = "{{ url_for(\'static\',filename=\'./flags/\') }}" + l + ".png"
                                a.img(src=flag_name, alt=l, klass="flags_index", align="left", name=l)
                with a.tr(klass='tr_flags_index'):
                    for l in lt[24:]:
                        with a.td(klass='td_flags_index'):
                            link_flag = url_for('team_stats', team_name=l)
                            with a.a(href=link_flag):
                                with a.p(klass='p_flags_index'):
                                    a(l)
                                flag_name = "{{ url_for(\'static\',filename=\'./flags/\') }}" + l + ".png"
                                a.img(src=flag_name, alt=l, klass="flags_index", align="left", name=l)

    # Casting the file to a string to extract the value
    html = str(a)
    # Casting the file to UTF-8 encoded bytes:
    html_bytes = bytes(a)
    print(html)
    h = open('templates/index.html', 'w')
    h.write(str(html))

    # close the file
    h.close()


if __name__ == "__main__":
    gen_HTML_index("Egypt")
    # survey({'Prueba': [19,10]}, ['Argentina', 'Chile'])
    # plt.show()