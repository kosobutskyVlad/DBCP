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

def get_loss_derivative(y_true, y_pred, parameters):
    offset = y_pred - y_true
    if offset < parameters[0]:
        return parameters[1]
    if offset < 0:
        return 0.01
    
    if offset < parameters[3]:
        return parameters[2]
    
    if offset < parameters[5]:
        return parameters[2] + parameters[4]
    
    return parameters[2] + parameters[4] + parameters[6]