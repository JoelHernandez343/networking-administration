import os

from flask import Flask, _app_ctx_stack
from sqlalchemy.orm import scoped_session

from database.manage import recreate_db
from database import SessionLocal, engine

try:
    os.remove("app/static/images/network.png")
except OSError:
    pass


recreate_db()

app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.session = scoped_session(SessionLocal, scopefunc=_app_ctx_stack.__ident_func__)

app.user = None
app.password = None


@app.teardown_appcontext
def remove_session(*args, **kwargs):
    print("Bye!")
    app.session.remove()


from .views import static_views, dynamyc_views
from . import requests
