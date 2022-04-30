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

class Holts():
    alpha1 = 0.01
    alpha2 = 0.01
    a = 0
    b = 0

    def __init__(self, alpha1=None, alpha2=None, a=None, b=None):
        if alpha1 is not None:
            self.alpha1 = alpha1
        if alpha2 is not None:
            self.alpha2 = alpha2
        if a is not None:
            self.a = a
        if b is not None:
            self.b = b

    def predict(self, y_true, dist=1):
        a_prev = self.a
        self.a = self.alpha1*y_true + (1-self.alpha1)*(self.a-self.b)
        self.b = self.alpha2*(self.a-a_prev) + (1-self.alpha2)*self.b
        return self.a + self.b*dist

    def fit(self, y, loss_params):
        best_loss = np.inf
        best_alpha = (0.01, 0.01)

        for alpha1 in np.arange(0.01, 1, 0.01):
            for alpha2 in np.arange(0.01, 1, 0.01):
                y_pred = []
                self.alpha1 = alpha1
                self.alpha2 = alpha2
                self.a = y[0]/2
                self.b = y[0]/2

                for y_true in y[:-1]:
                    y_pr = self.predict(y_true)
                    y_pred.append(y_pr)

                loss = sum(map(
                    get_loss, y[1:], y_pred, repeat(loss_params))
                ) / len(y - 1)

                if best_loss > loss:
                    best_loss = loss
                    best_alpha = alpha1, alpha2

        self.alpha1 = best_alpha[0]
        self.alpha2 = best_alpha[1]

class TrackingSignal():
    error_ema = EMA(0.05, 0)
    error_abs_ema = EMA(0.05, 0)
    
    alpha = 0.01
    y_prev = 0
    
    def predict(self, y_true):
        error = y_true - self.y_prev
        self.alpha = abs(self.error_ema.predict(error) / self.error_abs_ema.predict(abs(error)))
        self.y_prev = self.alpha*y_true + (1-self.alpha)*self.y_prev
        return self.y_prev
    
    def fit(self, y, loss_params):
        best_loss = np.inf
        best_g = (0.05, 0.05)

        for g1 in np.arange(0.05, 0.101, 0.005):
            for g2 in np.arange(0.05, 0.101, 0.005):
                y_pred = []
                self.error_ema = EMA(g1, 0)
                self.error_abs_ema = EMA(g2, 0)

                for y_true in y[:-1]:
                    y_pr = self.predict(y_true)
                    y_pred.append(y_pr)

                loss = sum(map(
                    get_loss, y[1:], y_pred, repeat(loss_params))
                ) / len(y - 1)

                if best_loss > loss:
                    best_loss = loss
                    best_g = g1, g2

        self.error_ema = EMA(best_g[0], 0)
        self.error_abs_ema = EMA(best_g[1], 0)