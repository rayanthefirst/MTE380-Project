import math

def scale_input(x, uppder_bound=1):
    # This function maps any real x to a value between 0 and 0.3 using a sigmoid formulation.
    return uppder_bound / (1 + math.exp(-x))