from data_prep_utils import prepare_data
from models.ema import EMA
from models.holts import Holts
from models.tracking_signal import TrackingSignal
from models.autoregression import Autoregression
from models.adaptive_composition import AdaptiveComposition

def predict(dataframe, aggr_window, loss_parameters):
    ema = EMA()
    holts = Holts()
    ts = TrackingSignal()
    ag = Autoregression(12)

    ac = AdaptiveComposition([ema, holts, ts, ag], "3D")
    X, y = prepare_data(dataframe, aggr_window)
    ac.fit(X, y, loss_parameters)

    y_pred = []

    for y_true in dataframe["sales"].values[:-1]:
        y_pr = ac.predict(y_true)
        y_pred.append(y_pr)

    return y_pred



