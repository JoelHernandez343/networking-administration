from flask import Flask, _app_ctx_stack, jsonify, url_for
from sqlalchemy.orm import scoped_session

from database import models, manage
from database.manage import router, interface, user
from database.database import SessionLocal, engine

models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)

app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.session = scoped_session(SessionLocal, scopefunc=_app_ctx_stack.__ident_func__)


@app.route("/")
def index():

    manage.recreate_db()

    r = {"name": "R1", "brand": "CISCO", "os": "Cisco OS"}
    interfaces = [
        {
            "name": "FastEthernet0/0",
            "ip": "1.1.1.1",
            "net": "1.1.1.0",
            "mask": "255.255.255.0",
            "is_active": True,
        },
        {
            "name": "FastEthernet0/1",
            "ip": "1.1.2.1",
            "net": "1.1.2.0",
            "mask": "255.255.255.0",
            "is_active": True,
        },
        {
            "name": "FastEthernet1/0",
            "ip": "1.1.3.1",
            "net": "1.1.3.0",
            "mask": "255.255.255.0",
            "is_active": True,
        },
    ]
    users = [
        {"name": "admin", "password": "admin"},
        {"name": "Vivian", "password": "yonofui"},
    ]

    router.add_w_interfaces_n_users(app.session, r, interfaces, users)

    res = {"before": router.get_all(app.session)}

    router.delete(app.session, "1.1.3.1")

    res["after"] = user.get_all(app.session)

    # res["after_after"] = router.get_all(app.session)

    return jsonify(res)

    # router = app.session.query(models.Router).get("1.1.1.4")

    # res = []
    # for interface in router.interfaces:
    #     res.append(interface.to_dict())

    # return jsonify(res)


@app.teardown_appcontext
def remove_session(*args, **kwargs):
    print("Bye!")
    app.session.remove()


# from app.views import static_views
# from app.views import dynamic_views
