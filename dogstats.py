import logging 

def calculate_average(input):
    """Calculate the average for a given list of numbers.

    Args:
        input (list): a list of numbers.
    """
    

    logging.warning("Input is: " + str(input))
    
    # Filter out None values from the list
    filtered_data = [x for x in input if x is not None]
    
    average = sum(filtered_data) / len(filtered_data)
    return round(average, 1)
    