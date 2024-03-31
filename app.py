from flask import Flask
from flask import render_template

from dogbase import overview, latest_activities, all_steps


app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html', message='Dog Stats')

@app.route('/overview')
def database():
    app.logger.warning("Calling overview endpoint")
    #return test_setup()
    return overview()

@app.route('/activities')
def activities():
    app.logger.warning("Calling activities endpoint")
    #return test_setup()
    return latest_activities(10)

@app.route('/daily')
def daily_steps():
    return all_steps()
