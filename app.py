from flask import Flask, render_template, request
import engine
import example1

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
	if request.method == "POST":
		playername = str(request.form['player'])
		team = str(request.form['team'])
		season = int(request.form['season'])
		month = str(request.form['month'])
		fullyear = str(season-1)+str(season)
		print fullyear
		location = 'h'
		event_types_key = [0,1,0]

		# links = example1.final(playername, team, season, month, fullyear, location, event_types_key)

		return render_template("index.html", playername = playername, season = season, month = month, links = example1.final(playername, team, season, month, fullyear, location, event_types_key))
	return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)

app = Flask(__name__)

