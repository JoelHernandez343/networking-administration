from .. import models, engine
from . import interface, router


def drop_db():
    models.Base.metadata.drop_all(bind=engine)


def create_db():
    models.Base.metadata.create_all(bind=engine)


def recreate_db(app):
    for thread in app.interface_threads:
        thread.stop()

    for thread in app.interface_threads:
        thread.join()

    drop_db()
    create_db()
