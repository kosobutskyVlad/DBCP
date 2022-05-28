from itertools import repeat

from numpy import arange

from forecasting.models.ema import EMA
from ..loss_function import get_loss

class TrackingSignal:
    """Tracking signal model"""
    
    def __init__(self):
        self.alpha = 0.01
        self.y_prev = 0
        self.error_ema = EMA(0.05, 0)
        self.error_abs_ema = EMA(0.05, 0)
        
    def predict(self, y_true):
        error = y_true - self.y_prev
        error_pred = self.error_abs_ema.predict(abs(error))
        if error_pred == 0:
            error_pred = 0.01
        self.alpha = abs(self.error_ema.predict(error) / error_pred)
        self.y_prev = self.alpha*y_true + (1-self.alpha)*self.y_prev
        return self.y_prev
    
    def fit(self, y, loss_params):
        best_loss = float('inf')

        for g1 in arange(0.05, 0.101, 0.005):
            for g2 in arange(0.05, 0.101, 0.005):
                y_pred = []
                best_g = g1, g2
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