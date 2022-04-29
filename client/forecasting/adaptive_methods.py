class EMA():
    alpha = 0
    y_pred = 0
    
    def __init__(self, alpha, y_pred):
        self.alpha = alpha
        self.y_pred = y_pred
        
    def predict(self, y_true):
        self.y_pred = self.alpha * y_true + (1-self.alpha) * self.y_pred
        return self.y_pred