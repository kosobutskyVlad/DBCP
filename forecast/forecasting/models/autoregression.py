from itertools import repeat
from typing import List

import numpy as np

from ..loss_function import get_loss_derivative

class Autoregression:
    """Autoregression model"""

    def __init__(self, feature_count: int) -> None:
        self.weights = np.zeros((feature_count,))
    
    def predict(self, X) -> float:
        return X.dot(self.weights.T)
    
    def fit(self, X: np.ndarray, y: np.ndarray, loss_params: List[float],
            step_size: float = 1e-5, n_iter: int = 100) -> None:

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