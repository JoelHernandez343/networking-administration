from database import models
from database.database import engine


from database.manage import user as user
from database.manage import router as router
from database.manage import interface as interface


def drop_db():
    models.Base.metadata.drop_all(bind=engine)


def create_db():
    models.Base.metadata.create_all(bind=engine)


def recreate_db():
    drop_db()
    create_db()
