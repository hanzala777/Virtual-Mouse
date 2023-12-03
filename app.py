# from flask import Flask, render_template, request
# import subprocess
#
# app = Flask(__name__, static_url_path='/static')
#
#
# @app.route('/')
# def index():
#     return render_template('home.html')
#
#
# @app.route('/run_python', methods=['POST'])
# def run_python():
#     # Execute your Python script (hello.py) using subprocess
#     subprocess.run(['python', 'final.py'])
#     return render_template('home.html')
#
#
# if __name__ == '__main__':
#     app.run(debug=False, host='0.0.0.0')

from flask import Flask, render_template, jsonify
import subprocess
import os

app = Flask(__name__)

# Global variable to store the subprocess ID
current_process = None


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/start_execution', methods=['POST'])
def start_execution():
    global current_process
    if current_process is None or current_process.poll() is not None:
        # If there is no running process or the previous process has completed, start a new one
        current_process = subprocess.Popen(['python', 'final.py'])


@app.route('/stop_execution', methods=['POST'])
def stop_execution():
    global current_process

    if current_process is not None and current_process.poll() is None:
        # If there is a running process, terminate it
        current_process.terminate()
        current_process = None


if __name__ == '__main__':
    app.run(debug=True)
