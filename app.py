from flask import Flask
from flask import render_template

from dogbase import overview, all_steps, steps_before_dog, steps_since_dog
from dogstats import calculate_average


app = Flask(__name__)

@app.route('/')
def homepage():
    # Define Plot Data 
    
    steps_with_dog = steps_since_dog()
    
    
    dates = []
    steps = []
    
    for entry in steps_with_dog:
        dates.append(entry)
        steps.append(steps_with_dog[entry])
        
    average_steps = calculate_average(steps)
 
    # Return the components to the HTML template 
    return render_template(
        template_name_or_list='index.html',
        data=steps,
        labels=dates,
        average=average_steps
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