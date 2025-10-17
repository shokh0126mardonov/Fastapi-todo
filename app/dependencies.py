from app.db.session import LocalSession


def get_db():
    return LocalSession()
