from flask import Flask, render_template, request
import engine
import example1
import json

app = Flask(__name__)

@app.route("/")
def home():
	return render_template("index.html")

@app.route("/single", methods=['GET', 'POST'])
def single():
	if request.method == "POST":
		playername = str(request.form['player'])
		team = str(request.form['team'])
		season = int(request.form['season'])
		month = int(request.form['month'])
		fullyear = str(season-1)+str(season)
		location = 'h'
		event_types_key = [0,1,0]
		active_event_types = engine.get_event_types(event_types_key)
		links = engine.single_player_search(playername, team, season, month, fullyear, location, event_types_key)

		urls = json.loads(links)['links']

		return render_template("single.html", playername = playername, season = season, active_event_types=active_event_types, month = month, urls = urls)
	return render_template("single.html")

if __name__ == '__main__':
    app.run(debug=True)

app = Flask(__name__)

