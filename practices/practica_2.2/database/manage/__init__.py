from database import models
from database.database import engine

from database.manage import interface
from database.manage import vlan


def drop_db():
    models.Base.metadata.drop_all(bind=engine)


def create_db():
    models.Base.metadata.create_all(bind=engine)


def recreate_db():
    drop_db()
    create_db()
