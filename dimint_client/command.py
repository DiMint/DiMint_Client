from functools import wraps
import json


def _after_processor(cmd):
    def wrap(func):
        @wraps(func)
        def return_func(*args, **kwargs):
            result = func(*args, **kwargs)
            if result is None:
                result = {}
            result['cmd'] = cmd
            return result
        return return_func
    return wrap


class Command:
    @classmethod
    @_after_processor('get_overlords')
    def get_overlords_list(cls):
        return None

    @classmethod
    @_after_processor('get')
    def get_by_key(cls, key, is_strong=False):
        cls.__validate_key(key)
        return {
            'key': key,
            'consistency': "strong" if is_strong else "week",
        }

    @classmethod
    @_after_processor('set')
    def set_value(cls, key, value):
        cls.__validate_key(key)
        cls.__validate_value(value)
        return {
            'key': str(key),
            'value': value,
        }

    @classmethod
    @_after_processor('state')
    def get_state(cls):
        return None

    @classmethod
    @_after_processor('overlord_state')
    def get_overlord_state(cls):
        return None

    @classmethod
    def __validate_key(cls, key):
        if not (isinstance(key, (int, float, str, bool)) or key is None):
            raise KeyError('Key must be immutable')

    @classmethod
    def __validate_value(cls, value):
        try:
            json.dumps(value)
        except TypeError:
            return ValueError('Value must can be transform to json')
