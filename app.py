from flask import Flask
from flask import render_template

from dogbase import overview, all_steps, steps_before_dog, steps_since_dog


app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html', message='Dog Stats')

@app.route('/overview')
def database():
    app.logger.warning("Calling overview endpoint")
    #return test_setup()
    return overview()

@app.route('/daily')
def daily_steps():
    return all_steps()

@app.route('/before')
def steps_without_dog():
    return steps_before_dog()

@app.route('/after')
def steps_after_dog():
    return steps_since_dog()