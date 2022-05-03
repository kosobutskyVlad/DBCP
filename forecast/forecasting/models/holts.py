from itertools import repeat

import numpy as np

from forecasting.models.base import Model
from ..loss_function import get_loss

class Holts(Model):
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

        for alpha1 in np.arange(0.05, 1, 0.05):
            for alpha2 in np.arange(0.05, 1, 0.05):
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