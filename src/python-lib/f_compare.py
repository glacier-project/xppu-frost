import numpy as np

EPS = np.finfo(float).eps

def are_nearly_equal(n1: float, n2: float, relative_error=1e-2, min=np.finfo(float).min):
    if not np.isfinite(n1) or not np.isfinite(n2):
        return False

    diff = np.abs(n1-n2)
    if diff < min:
        return True

    return (diff / max(np.abs(n1),np.abs(n2))) <= relative_error

def approximately_zero(n1: float, eps:float = EPS):
    return np.abs(n1) <= eps

def approximately_equal(n1: float, n2: float, eps:float = EPS):
    return np.abs(n1-n2) <= (np.abs(n2) if np.abs(n1)<np.abs(n2) else np.abs(n1))*eps

def essentially_equal(n1: float, n2: float, eps:float = EPS):
    return np.abs(n1-n2) <= (np.abs(n2) if np.abs(n1)>np.abs(n2) else np.abs(n1))*eps

def definitely_greater_than(n1: float, n2: float, eps:float = EPS):
    return (n2-n1) <= (np.abs(n2) if np.abs(n1)>np.abs(n2) else np.abs(n1))*eps

def definitely_less_than(n1: float, n2: float, eps:float = EPS):
    return (n1-n2) <= (np.abs(n2) if np.abs(n1)>np.abs(n2) else np.abs(n1))*eps

def cos(n, eps:float = EPS):
    cos = np.cos(n)
    if approximately_zero(cos, eps):
        return 0
    if approximately_equal(cos, 1, eps):
        return 1
    if approximately_equal(cos, -1, eps):
        return -1
    return cos

def sin(n, eps:float = EPS):
    sin = np.sin(n)
    if approximately_zero(sin, eps):
        return 0
    if approximately_equal(sin, 1, eps):
        return 1
    if approximately_equal(sin, -1, eps):
        return -1
    return sin

def round(n, decimals=12):
    return np.round(n, decimals=decimals)
