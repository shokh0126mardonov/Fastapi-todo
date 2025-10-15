from db import LocalSession


def get_db():
    return LocalSession()
