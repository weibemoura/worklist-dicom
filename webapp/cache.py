import os
import pickle

from decouple import config


def get_data():
    data = []
    try:
        with open(config("CACHE_FILE"), "rb") as cache:
            data = pickle.load(cache)
    except Exception as _:
        pass
    return data


def write_data(data):
    with open(config("CACHE_FILE"), "wb") as cache:
        pickle.dump(data, cache, pickle.HIGHEST_PROTOCOL)


def invalidate():
    os.remove(config("CACHE_FILE"))


def exists():
    return os.path.exists(config("CACHE_FILE"))
