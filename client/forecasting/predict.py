from forecasting.data_prep_utils import prepare_data
from forecasting.models.ema import EMA
from forecasting.models.holts import Holts
from forecasting.models.tracking_signal import TrackingSignal
from forecasting.models.autoregression import Autoregression
from forecasting.models.adaptive_composition import AdaptiveComposition

def predict(dataframe, aggr_window, loss_parameters):
    ema = EMA()
    holts = Holts()
    ts = TrackingSignal()
    ag = Autoregression(12)

    ac = AdaptiveComposition([ema, holts, ts, ag], "3D")
    X, y = prepare_data(dataframe, aggr_window)
    ac.fit(X, y, loss_parameters)

    y_pred = []

    for i, y_true in enumerate(y):
        y_pr = ac.predict(X[i], y_true)
        y_pred.append(y_pr)

    return y_pred



