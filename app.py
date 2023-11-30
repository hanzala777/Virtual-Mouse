from flask import Flask, render_template, request
import subprocess

app = Flask(__name__, static_url_path='/static')


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/run_python', methods=['POST'])
def run_python():
    # Execute your Python script (hello.py) using subprocess
    subprocess.run(['python', 'final.py'])
    return 'Python script executed successfully.'


if __name__ == '__main__':
    app.run(debug=True)
