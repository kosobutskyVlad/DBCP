from itertools import repeat

import numpy as np

from forecasting.models.base import Model
from ..loss_function import get_loss

class EMA(Model):
    alpha = 0.01
    y_prev = 0

    def __init__(self, alpha=None, y_prev=None):
        if alpha is not None:
            self.alpha = alpha
        if y_prev is not None:
            self.y_prev = y_prev

    def predict(self, y_true):
        self.y_prev = self.alpha*y_true + (1-self.alpha)*self.y_prev
        return self.y_prev

    def fit(self, y, loss_params):
        best_loss = np.inf
        best_alpha = 0.01
    
        for alpha in np.arange(0.05, 1, 0.05):
            y_pred = []
            self.alpha = alpha
            self.y_prev = y[0]
            
            for y_true in y[:-1]:
                y_pr = self.predict(y_true)
                y_pred.append(y_pr)
            
            loss = sum(map(
                get_loss, y[1:], y_pred, repeat(loss_params))
            ) / len(y - 1)
            
            if best_loss > loss:
                best_loss = loss
                best_alpha = alpha
        
        self.alpha = best_alpha