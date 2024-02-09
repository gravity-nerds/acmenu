def paramDefault(kwargs, id, default):
    if id in kwargs:
        return kwargs[id]
    return default

def lerp(a, b, t):
    return a + (b - a) * t