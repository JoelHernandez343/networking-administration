from database import models
from database.database import engine


def drop_db():
    models.Base.metadata.drop_all(bind=engine)


def create_db():
    models.Base.metadata.create_all(bind=engine)


def recreate_db():
    drop_db()
    create_db()
