import numpy as np

# def scale_input(x, upper_bound=1):
#     return upper_bound / (1 + np.exp(-x))


def scale_input(x, upper_bound=1):
    return x / upper_bound

