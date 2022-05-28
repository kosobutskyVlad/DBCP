from itertools import repeat
from types import NoneType
from typing import List

from numpy import arange

from ..loss_function import get_loss

class Holts:
    """Holts linear trend model"""

    def __init__(self, alpha1: float = 0.01, alpha2: float = 0.01,
                 a: float = 0, b: float = 0) -> None:

        self.alpha1 = alpha1
        self.alpha2 = alpha2
        self.a = a
        self.b = b

    def predict(self, y_true: float, dist: int = 1) -> float:
        a_prev = self.a
        self.a = self.alpha1*y_true + (1-self.alpha1)*(self.a-self.b)
        self.b = self.alpha2*(self.a-a_prev) + (1-self.alpha2)*self.b
        return self.a + self.b*dist

    def fit(self, y: float, loss_params: List[float]) -> None:
        best_loss = float('inf')
        best_alpha = (0.01, 0.01)

        for alpha1 in arange(0.05, 1, 0.05):
            for alpha2 in arange(0.05, 1, 0.05):
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