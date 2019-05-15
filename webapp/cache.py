import os as _os
import pickle as _pickle

from decouple import config as _config


def get_data():
    data = []
    try:
        with open(_config("CACHE_FILE"), "rb") as cache:
            data = _pickle.load(cache)
    except Exception as _:
        pass
    return data


def write_data(data):
    with open(_config("CACHE_FILE"), "wb") as cache:
        _pickle.dump(data, cache, _pickle.HIGHEST_PROTOCOL)


def invalidate():
    _os.remove(_config("CACHE_FILE"))


def exists():
    return _os.path.exists(_config("CACHE_FILE"))
