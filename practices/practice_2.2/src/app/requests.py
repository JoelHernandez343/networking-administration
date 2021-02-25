from pexpect.pxssh import ExceptionPxssh

from flask import request, jsonify

from app import app

import networking
from database.manage import vlan, recreate_db, interface


@app.route("/request", methods=["POST"])
def request_information():

    if request.is_json:
        req = request.get_json()

        if req["type"] == "login":
            return set_login(app.session, req["user"])

        if req["type"] == "vlans":
            return get_all_vlans(app.session)

        if req["type"] == "scan":
            return scan(app.session)

        if req["type"] == "switches":
            return get_all_switches(app.session)

        if req["type"] == "add":
            return add_vlan(app.session, req["vlan"])

        if req["type"] == "delete":
            return delete_vlan(app.session, req["vlan_number"])

    return jsonify({"message": "This petition doesn't have a response"}), 400


def get_all_vlans(db):
    return jsonify(vlan.get_all(db))


def scan(db):
    recreate_db()

    try:
        vlans = networking.get_vlans({"name": app.user, "password": app.password})
        for v in vlans:
            vlan.add(db, v)

        return jsonify({"message": "ok"})
    except Exception as err:
        return jsonify({"message": str(err)}), 500


def get_all_switches(db):
    switches = interface.to_switch_structure(interface.get_all(db))

    return jsonify(switches)


def add_vlan(db, v):

    if vlan.get(db, v["number"]) is not None:
        return jsonify({"message": f"This vlan {v['number']} already exits!"}), 400

    v["gateway"] = networking.net.get_first_ip(v["net"], v["mask"])

    networking.set_vlan(v, {"name": app.user, "password": app.password})
    vlan.add(db, v)

    return jsonify({"message": "ok"})


def delete_vlan(db, v_number):
    if v_number == 1:
        return jsonify({"message": "Cannot erase VLAN1"}), 400

    v = vlan.get(db, v_number)

    if v is None:
        return jsonify({"message": f"This vlan {v_number} doesn't exists!"}), 400

    networking.set_vlan(v, {"name": app.user, "password": app.password}, delete=True)
    vlan.delete(db, v_number)

    return jsonify({"message": "ok"})


def set_login(db, user):

    try:

        devices = ["192.168.1.11", "192.168.1.12", "192.168.1.13", "192.168.1.1"]

        for d in devices:
            session = networking.connection.create(d, user)

        app.user = user["name"]
        app.password = user["password"]

        return jsonify({"message": "ok"})

    except ExceptionPxssh as err:
        return jsonify({"message": str(err)}), 500
