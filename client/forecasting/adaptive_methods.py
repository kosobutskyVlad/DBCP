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
    y_pred = 0

    def __init__(self, alpha, y_pred):
        self.alpha = alpha
        self.y_pred = y_pred

    def predict(self, y_true):
        self.y_pred = self.alpha * y_true + (1-self.alpha) * self.y_pred
        return self.y_pred