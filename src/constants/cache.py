from flask import request

USER_ORDERS_CACHE_KEY = 'user_orders'


def make_user_orders_cache_key():
    return USER_ORDERS_CACHE_KEY + '_page_' + request.args.get('page')
