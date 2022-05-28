import numpy as np

from forecasting.models.ema import EMA
from forecasting.models.autoregression import Autoregression

class AdaptiveComposition:
    """Weighted composition"""
    
    def __init__(self, models, aggr_window=None):
        self.models = []
        self.errors_ema = []
        for model in models:
            self.models.append(model)
            self.errors_ema.append(EMA(0.05, 0.01))
        self.predictions = np.full((len(self.models), ), fill_value=1)
        self.aggr_window = aggr_window
    
    def predict(self, X, y):
        
        err_pred = np.full((len(self.models), ), fill_value=0.01)
        for i, err_ema in enumerate(self.errors_ema):
            err = y - self.predictions[i]

            err_pred[i] = err_ema.predict(err)
            if err_pred[i] == 0:
                err_pred[i] = 0.01

        weights = [1/abs(err) for err in err_pred]
        weights = np.array([w/sum(weights) for w in weights])
        self.predictions = np.full((len(self.models), ), fill_value=0)
        for i, model in enumerate(self.models):
            if isinstance(model, Autoregression):
                self.predictions[i] = model.predict(X)
            else:
                self.predictions[i] = model.predict(y)

        return np.dot(self.predictions, weights.T)
    
    def fit(self, X, y, loss_params):
        for model in self.models:
            if isinstance(model, Autoregression):
                if self.aggr_window is None:
                    raise ValueError("Specify aggr_window if using Autoregression")
                print(model.weights)
                model.fit(X, y, loss_params)
            else:
                model.fit(y, loss_params)