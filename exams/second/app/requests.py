import json

from flask import make_response

from app import app
from app.views import routing

import networking


@app.route("/requests/discover_topology", methods=["POST"])
def discover_topology():
    try:
        networking.discover_topology(app.session)
        app.routes = routing.build_routing(app.session)

        return make_response(json.dumps({"message": "ok"}), 200)

    except Exception as e:
        obj = {"message": str(e)}
        return make_response(json.dumps(obj), 500)
