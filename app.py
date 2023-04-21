from flask import Flask, render_template, request, make_response
from generate_html_team import gen_HTML
from generate_html_index import gen_HTML_index
from generate_html_match import gen_HTML_match
from generate_html_players import gen_HTML_players

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# Defining the home page of our site
team_name = ''
@app.route('/')
def load():
    gs = gen_HTML_index("England")
    return render_template("index.html")

@app.route('/team_stats/<team_name>')
def team_stats(team_name):
    get_team = team_name
    p_stats = gen_HTML_players(get_team)
    new_team_selected = gen_HTML(get_team)
    new_team_selected_match = gen_HTML_match(get_team)
    return render_template("team_stats.html")

@app.route('/team_stats')
def team_stats2():
    return render_template("team_stats.html")

@app.route('/players_stats')
def players_stats():
    return render_template("players_stats.html")

@app.route('/match_stats')
def match_stats():
    return render_template("match_stats.html")

@app.route('/', methods=['POST'])
def load_team():
    if request.method == 'POST':
        get_team = request.form['combo_team']
    p_stats = gen_HTML_players(get_team)
    new_team_selected = gen_HTML(get_team)
    new_team_selected_match = gen_HTML_match(get_team)
    return render_template("team_stats.html")

if __name__ == "__main__":
    app.run(debug=True)