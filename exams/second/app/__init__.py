from flask import Flask, _app_ctx_stack, jsonify, url_for
from sqlalchemy.orm import scoped_session

from app.views import routing

from database import models, manage
from database.manage import router, interface, user
from database.database import SessionLocal, engine

manage.recreate_db()

app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.session = scoped_session(SessionLocal, scopefunc=_app_ctx_stack.__ident_func__)

# r = {"name": "R1", "brand": "CISCO", "os": "Cisco OS"}
# interfaces = [
#     {
#         "name": "FastEthernet0-0",
#         "ip": "1.1.1.1",
#         "net": "1.1.1.0",
#         "mask": "255.255.255.0",
#         "is_active": True,
#     },
#     {
#         "name": "FastEthernet0-1",
#         "ip": "1.1.2.1",
#         "net": "1.1.2.0",
#         "mask": "255.255.255.0",
#         "is_active": True,
#     },
#     {
#         "name": "FastEthernet1-0",
#         "ip": "1.1.3.1",
#         "net": "1.1.3.0",
#         "mask": "255.255.255.0",
#         "is_active": True,
#     },
# ]
# users = [
#     {"name": "admin"},
#     {"name": "Vivian"},
# ]

# r2 = {"name": "R2", "brand": "CISCO", "os": "Cisco OS"}
# interfaces2 = [
#     {
#         "name": "FastEthernet0-0",
#         "ip": "1.1.1.2",
#         "net": "1.1.1.0",
#         "mask": "255.255.255.0",
#         "is_active": True,
#     },
#     {
#         "name": "FastEthernet0-1",
#         "ip": "1.1.2.2",
#         "net": "1.1.2.0",
#         "mask": "255.255.255.0",
#         "is_active": True,
#     },
# ]

# router.add_w_interfaces_n_users(app.session, r, interfaces, users)
# router.add_w_interfaces_n_users(app.session, r2, interfaces2, users)

app.routes = routing.build_routing(app.session)


@app.teardown_appcontext
def remove_session(*args, **kwargs):
    print("Bye!")
    app.session.remove()


from app.views import static_views
from app.views import dynamic_views
from app import requests