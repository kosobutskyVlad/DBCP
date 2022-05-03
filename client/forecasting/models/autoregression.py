from itertools import repeat

import numpy as np

from base import Model
from ..loss_function import get_loss_derivative

class Autoregression(Model):
    weights = None

    def __init__(self, feature_count):
        self.weights = np.zeros((feature_count,))
    
    def predict(self, X):
        return X.dot(self.weights.T)
    
    def fit(self, X, y, loss_params, step_size=1e-5, n_iter=100):
        for _ in range(n_iter):
            y_pred = self.predict(X)
            loss_der = np.array(list(map(
                get_loss_derivative,
                y[1:], 
                y_pred,
                repeat(loss_params)
            )))
            gradient = X[1:].T.dot(loss_der) / (y.shape[0]-1)
            self.weights -= gradient*step_size