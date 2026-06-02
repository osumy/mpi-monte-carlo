import math
import numpy as np

class MonteCarloIntegrator:
    def __init__(self, upper_bound):
        self.upper_bound = upper_bound

    def get_exact_value(self):
        return 1.0 - math.cos(self.upper_bound)

    def calculate_local_sum(self, n_samples):
        if n_samples <= 0:
            return 0.0
        points = np.random.uniform(0.0, self.upper_bound, n_samples)
        return np.sum(np.sin(points))