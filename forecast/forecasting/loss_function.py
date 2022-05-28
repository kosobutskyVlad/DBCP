from typing import List

def get_loss(y_true: float, y_pred: float, params: List[float]) -> float:
    offset = y_pred - y_true
    if offset < params[0]:
        return (offset-params[0])*params[1]
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

def get_loss_derivative(y_true: float, y_pred: float,
                        params: List[float]) -> float:
    offset = y_pred - y_true
    if offset < params[0]:
        return params[1]
    if offset < 0:
        return 0.01
    
    if offset < params[3]:
        return params[2]
    
    if offset < params[5]:
        return params[2] + params[4]
    
    return params[2] + params[4] + params[6]