from src.constants.status_codes import OK_CODE


def make_cache_invalidator(cache, cache_key):
    def _inner(request, body, status):
        if request.method.lower() in ['put', 'post', 'delete'] and status == OK_CODE:
            cache.delete(cache_key)

    return _inner


def response_filter(res):
    return res[1] == OK_CODE
