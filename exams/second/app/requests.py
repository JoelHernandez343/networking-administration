import json

from flask import make_response

from app import app
from app.views import routing
from database import manage
import networking

from flask import render_template, jsonify, request

from database.manage import router as rt, interface as intf, user


@app.route("/requests/discover_topology", methods=["POST"])
def discover_topology():
    try:
        manage.recreate_db()

        networking.discover_topology(app.session)
        app.routes = routing.build_routing(app.session)

        return make_response(json.dumps({"message": "ok"}), 200)

    except Exception as e:
        obj = {"message": str(e)}
        return make_response(json.dumps(obj), 500)


@app.route("/requests/<router>", methods=["POST"])
def get_information_router(router):

    r = rt.get(app.session, router)

    if r is None:
        return jsonify({"message": f"This router {router} doesnt exist"}), 404

    if request.is_json:
        print("HELLO")
        req = request.get_json()

        if req["type"] == "router":
            return jsonify(r)

        if req["type"] == "modify":
            return modify_router(app.session, router, req["hostname"])

    return (
        jsonify({"message": f"This petition {req['type']} doesnt have response"}),
        404,
    )


def modify_router(db, router_id, hostname):
    try:
        networking.change_hostname(router_id, hostname)
        rt.modify(app.session, router_id, hostname=hostname)

        app.routes = routing.build_routing(app.session)

        return jsonify({"message": "ok"})
    except Exception as e:
        return jsonify({"message": e.message}), 500
