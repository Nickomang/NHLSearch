from flask import Flask, render_template
import engine
import example1

app = Flask(__name__)

@app.route("/")
def main():
    return render_template('index.html')

@app.route('/search')
def search():
	return flask.jsonify(**example1)
    # if request.method == "POST":
    #     return example2
    # return render_template('search.html')

# ERROR HANDLING
@app.errorhandler(404)
def pageNotFound(error):
    return "it didnt work"

@app.errorhandler(500)
def pageNotFound(error):
    return "internal server error"

if __name__ == "__main__":
    app.run()