from flask import Flask
from flask import render_template

from dogbase import overview, all_steps, steps_before_dog, steps_since_dog


app = Flask(__name__)

@app.route('/')
def homepage():
    # Define Plot Data 
    
    steps_with_dog = steps_since_dog()
    
    
    labels = []
    data = []
    
    for entry in steps_with_dog:
        labels.append(entry)
        data.append(steps_with_dog[entry])
 
    # Return the components to the HTML template 
    return render_template(
        template_name_or_list='index.html',
        data=data,
        labels=labels,
    )


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

# Main Driver Function 
if __name__ == '__main__':
    # Run the application on the local development server ##
    app.run(debug=True)