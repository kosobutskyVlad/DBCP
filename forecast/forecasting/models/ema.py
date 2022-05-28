from itertools import repeat
from typing import List

from numpy import arange

from ..loss_function import get_loss

class EMA:
    """Exponential moving average"""

    def __init__(self, alpha: float = 0.01, y_prev: float = 0) -> None:
        self.alpha = alpha
        self.y_prev = y_prev

    def predict(self, y_true: float) -> float:
        self.y_prev = self.alpha*y_true + (1-self.alpha)*self.y_prev
        return self.y_prev

    def fit(self, y: float, loss_params: List[float]) -> None:
        best_loss = float('inf')
        best_alpha = 0.01
    
        for alpha in arange(0.05, 1, 0.05):
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