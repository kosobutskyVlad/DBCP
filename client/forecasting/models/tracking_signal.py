from itertools import repeat

import numpy as np

from forecasting.models.base import Model
from forecasting.models.ema import EMA
from ..loss_function import get_loss

class TrackingSignal(Model):
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

        for g1 in np.arange(0.05, 0.101, 0.005):
            for g2 in np.arange(0.05, 0.101, 0.005):
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