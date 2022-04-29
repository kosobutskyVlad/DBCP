from itertools import repeat

import numpy as np

def get_loss(y_true, y_pred, params):
    offset = y_pred - y_true
    if offset < params[0]:
        return offset*params[1]
    if offset < 0:
        return 0

    if offset < params[3]:
        return offset*params[2]

    if offset < params[5]:
        return (params[2]*params[3]
                + (offset - params[3])*(params[2] + params[4]))

    return (params[2]*params[3]
            + (params[5] - params[3])*(params[2] + params[4])
            + (offset - params[5])*(params[2] + params[4] + params[6]))

class EMA():
    alpha = 0
    y_prev = 0

    def __init__(self, alpha, y_prev):
        self.alpha = alpha
        self.y_prev = y_prev

    def predict(self, y_true):
        self.y_prev = self.alpha*y_true + (1-self.alpha)*self.y_prev
        return self.y_prev

    def fit(self, y, loss_params):
        best_loss = np.inf
        best_alpha = 0.01
    
        for alpha in np.arange(0.01, 1, 0.01):
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