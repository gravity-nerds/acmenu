def paramDefault(kwargs, id, default):
    if id in kwargs:
        return kwargs[id]
    return default