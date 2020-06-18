def find_in_array(arr, cb):
    for i, el in enumerate(arr):
        if cb(el):
            return i, el

    return -1, None
