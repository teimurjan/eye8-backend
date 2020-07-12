from src.constants.status_codes import OK_CODE


class CategoryProductTypesCache:
    def __init__(self, cache):
        self._cache = cache
        self.__prefix = 'category_product_types'

    def __get_cache_keys(self):
        # Should be changed in case of using different cache type
        return [k for k in self._cache.cache._cache.keys() if k.startswith(self.__prefix)]

    def invalidate(self):
        self._cache.delete_many(*self.__get_cache_keys())

    def get_invalidate_hook(self):
        def hook(request, body, status):
            if request.method.lower() in ['put', 'post', 'delete'] and status == OK_CODE:
                self.invalidate()

        return hook

    def make_cache_key(self, category_slug):
        from flask import request
        return (
            self.__prefix +
            '_slug_' +
            category_slug +
            '_page_' +
            request.args.get('page', 'None') +
            '_limit_' +
            request.args.get('limit', 'None') +
            '_sort_by_' +
            request.args.get('sort_by', 'None')
        )
