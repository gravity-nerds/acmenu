def paramDefault(kwargs, id, default):
    if id in kwargs:
        return kwargs[id]
    return default

def lerp(a, b, t):
    return a + (b - a) * t

def clamp(x, mi, ma):
    return max(mi, min(x, ma))