from flask import request, jsonify
from pexpect.pxssh import ExceptionPxssh
from app import app

from database.manage import recreate_db

from networking import ssh, topology, snmp

from database.manage import router as rt, interface as it, register as rg


@app.route("/request", methods=["POST"])
def request_information():

    if request.is_json:
        req = request.get_json()

        if req["type"] == "login":
            return set_login(app.session, req["user"])

        if req["type"] == "updateDb":
            return update_all(app.session, {"name": app.user, "password": app.password})

        if req["type"] == "changeHostname":
            return change_hostname(app.session, req["router"])

        if req["type"] == "registers":
            return get_registers(app.session, req["interface"])

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
        recreate_db(app)

        topology.discover(db, user)

        return jsonify({"message": "ok"})

    except Exception as err:
        return jsonify({"message": str(err)}), 500


def change_hostname(db, router):
    try:
        r = rt.get(db, router["id"])

        if r is None:
            return (
                jsonify({"message": f"This router {router['id']} doesn't exist."}),
                404,
            )

        rt.modify(db, router["id"], router["newHostname"])
        snmp.configuration.set_hostname(r["accesible_ip"], router["newHostname"])

        return jsonify({"message": "ok"})

    except Exception as err:
        return jsonify({"message": str(err)}), 500


def get_registers(db, interface):
    try:

        registers = rg.get_all(db, interface)

        return jsonify({"registers": registers})

    except Exception as err:
        return jsonify({"message": str(err)}), 500
