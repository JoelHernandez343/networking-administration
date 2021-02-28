import os

from flask import Flask, _app_ctx_stack, render_template
from sqlalchemy.orm import scoped_session

from app.views import routing

from database import models, manage
from database.manage import router, interface, user
from database.database import SessionLocal, engine

try:
    os.remove("src/app/static/images/network.png")
except OSError:
    pass

manage.recreate_db()

app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.session = scoped_session(SessionLocal, scopefunc=_app_ctx_stack.__ident_func__)

app.routes = routing.build_routing(app.session)


@app.teardown_appcontext
def remove_session(*args, **kwargs):
    print("Bye!")
    app.session.remove()


from app.views import static_views
from app.views import dynamic_views
from app import requests
