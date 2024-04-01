
def calculate_average(input):
    """Calculate the average for a given list of numbers.

    Args:
        input (list): a list of numbers.
    """
    
    if input[-1] == None:
        del input[-1]
    
    average = sum(input) / len(input)
    return round(average, 1)
    