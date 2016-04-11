# import flask
from flask import Flask, render_template, request

# initilize flask
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        player = int(request.form['player'])
        return render_template('index.html', playername = player)
    return render_template('index.html')

# run the server
if __name__ == '__main__':
    app.run(debug=True)