from flask import request, jsonify
from pexpect.pxssh import ExceptionPxssh

from app import app

from database import models
from database.manage import recreate_db, router as rt, interface as it, register as rg

from networking import ssh, topology, snmp


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

        if req["type"] == "lostPackages":
            return check_lost_packages(
                app.session,
                req["interface"],
                req["percentage"],
                {"name": app.user, "password": app.password},
            )

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


def check_lost_packages(db, interface, percentage, user):
    try:
        i_source = it.get(
            db, {"router_id": interface["router_id"], "name": interface["name"]}
        )

        next_hop = ssh.information.check_next_connection(i_source, user)

        if next_hop is None:
            return (
                jsonify(
                    {
                        "message": f"This interface {i_source['name']} of router {i_source['router_id']} doesn't has next hop"
                    }
                ),
                404,
            )

        i_dest = {}
        for i in db.query(models.Interface).filter(models.Interface.ip == next_hop):
            i_dest = i.to_dict()

        is_exceeded, percentage = snmp.information.check_lost_percentage(
            i_source, i_dest, percentage
        )

        return jsonify({"isExceeded": is_exceeded, "percentage": percentage})

    except Exception as err:
        return jsonify({"message": str(err)}), 500
