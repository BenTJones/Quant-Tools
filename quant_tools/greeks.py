from simulations import mc_european_call

def greeks_estimate(method, bump = 1e-2,**kwargs):
    if method == 'vega':
        param = 'sigma'
        h = kwargs[param] * bump
    elif method == 'theta':
        param = 'T'
        h = bump
    elif method == 'delta':
        param = 's0'
        h = kwargs[param] * bump
    elif method == 'rho':
        param = 'r'
        h = bump
    else:
        raise ValueError('Invalid greeks method')

    param_val = kwargs.pop(param)
    pos_bump = param_val + h
    neg_bump = param_val - h
    pos_kwargs = {**kwargs , param : pos_bump}
    neg_kwargs = {**kwargs , param : neg_bump}
    pos_mc= mc_european_call(**pos_kwargs)
    neg_mc = mc_european_call(**neg_kwargs)
    greeks = (pos_mc - neg_mc) / (2 * h)
    return greeks

