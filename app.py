from flask import Flask
from flask import render_template

from dogbase import overview, all_steps, steps_before_dog, steps_since_dog
from dogstats import calculate_average


app = Flask(__name__)

@app.route('/')
def homepage():
    variables_for_html = {}
    
    # Define Plot Data 
    # Data with dog
    data_with_dog = steps_since_dog()
    dates_with_dog = []
    steps_with_dog = []
        
    for entry in data_with_dog:
        dates_with_dog.append(entry)
        steps_with_dog.append(data_with_dog[entry])
                
    average_steps_with_dog = calculate_average(steps_with_dog)
    
    
    # Data without dog
    data_without_dog = steps_before_dog()
    dates_without_dog = []
    steps_without_dog = []
    
    for entry in data_without_dog:
        dates_without_dog.append(entry)
        steps_without_dog.append(data_without_dog[entry])
        
    average_steps_without_dog = calculate_average(steps_without_dog)
    
    
 
    # Return the components to the HTML template 
    return render_template(
        template_name_or_list='index.html',
        dataWithDog=steps_with_dog,
        labelsWithDog=dates_with_dog,
        averageWithDog=average_steps_with_dog,
        
        dataNoDog=steps_without_dog,
        labelsNoDog=dates_without_dog,
        averageNoDog=average_steps_without_dog
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