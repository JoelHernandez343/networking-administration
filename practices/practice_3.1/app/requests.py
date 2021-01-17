from flask import request, jsonify
from pexpect.pxssh import ExceptionPxssh
from app import app

from database.manage import recreate_db

from networking import ssh, topology


@app.route("/request", methods=["POST"])
def request_information():

    if request.is_json:
        req = request.get_json()

        if req["type"] == "login":
            return set_login(app.session, req["user"])

        if req["type"] == "updateDb":
            return update_all(app.session, {"name": app.user, "password": app.password})

        # if req["type"] == "vlans":
        #     return get_all_vlans(app.session)

        # if req["type"] == "scan":
        #     return scan(app.session)

        # if req["type"] == "switches":
        #     return get_all_switches(app.session)

        # if req["type"] == "add":
        #     return add_vlan(app.session, req["vlan"])

        # if req["type"] == "delete":
        #     return delete_vlan(app.session, req["vlan_number"])

    return jsonify({"message": "This petition doesn't have a response"}), 400


def set_login(db, user):
    try:
        devices = [ssh.tools.get_default_gateway()]

        for d in devices:
            session = ssh.connection.create(d, user)

        app.user = user["name"]
        app.password = user["password"]

        return jsonify({"message": "ok"})

    except ExceptionPxssh as err:
        return jsonify({"message": str(err)}), 500


def update_all(db, user):
    try:
        recreate_db()

        topology.discover(db, user)

        return jsonify({"message": "ok"})

    except ExceptionPxssh as err:
        return jsonify({"message": str(err)}), 500
