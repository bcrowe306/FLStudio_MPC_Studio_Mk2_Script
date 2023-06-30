def contains(list, filter):
    for x in list:
        if filter(x):
            return True
    return False


def get_index(list, name):
    for index, item in enumerate(list):
        if item.name == name:
            return index
    else:
        return -1

def safe_getattr(obj, name, default=None):
    try:
        return getattr(obj, name, default)
    except Exception:  # or your specific exceptions
        return default
