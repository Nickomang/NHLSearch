import threading
import subprocess
import uuid
from flask import Flask
from flask import render_template, url_for, abort, jsonify, request
app = Flask(__name__)


# def run_script(id):
#     subprocess.call(["engine.py", "argument1", "argument2"])
#     background_scripts[id] = True

@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/generate')
# def generate():
#     id = str(uuid.uuid4())
#     background_scripts[id] = False
#     threading.Thread(target=lambda: run_script(id)).start()
#     return render_template('processing.html', id=id)

# @app.route('/test')
# def test():
# 	return render_template('test.html')

# @app.route('/is_done')
# def is_done():
#     id = request.args.get('id', None)
#     if id not in background_scripts:
#         abort(404)
#     return jsonify(done=background_scripts[id])

if __name__ == "__main__":
    app.run()