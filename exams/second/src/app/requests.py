import json

from flask import make_response

from app import app
from app.views import routing
from database import manage
import networking

from pexpect.exceptions import TIMEOUT

from flask import render_template, jsonify, request

from database.manage import router as rt, interface as intf, user as usr


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
        req = request.get_json()

        if req["type"] == "router":
            return jsonify(r)

        if req["type"] == "modify":
            return modify_router(app.session, router, req["hostname"])

    return (
        jsonify({"message": f"This petition {req['type']} doesnt have response"}),
        404,
    )


@app.route("/requests/<router>/<interface>", methods=["POST"])
def get_information_interface(router, interface):
    r = rt.get(app.session, router)
    if r is None:
        return jsonify({"message": f"This router {router} doesnt exist"}), 404

    i = intf.get(app.session, {"router_id": router, "name": interface})
    if i is None:
        return (
            jsonify(
                {"message": f"This interface {interface} doesnt exist in {router}"}
            ),
            404,
        )

    if request.is_json:
        req = request.get_json()

        if req["type"] == "information":
            return jsonify(i)

        if req["type"] == "modify":
            changes = req["changes"]
            return modify_interface(
                app.session, {"router_id": router, "name": interface}, changes
            )

    return (
        jsonify({"message": f"This petition {req['type']} doesnt have response"}),
        404,
    )


@app.route("/requests/users/<router>", methods=["POST"])
def users_routers(router):
    r = rt.get(app.session, router)
    if r is None:
        return jsonify({"message": f"This router {router} doesnt exist"}), 404

    if request.is_json:
        req = request.get_json()

        if req["type"] == "create":
            return create_user(app.session, router, req["user"])

        if req["type"] == "delete":
            return delete_user(app.session, router, req["user"])

        if req["type"] == "modify":
            return modify_user(app.session, router, req["user"])

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
        return jsonify({"message": str(e)}), 500


def modify_interface(db, interface, changes):
    try:

        try:
            networking.toggle_interface(
                interface["router_id"],
                networking.net.translate_to_router(interface["name"]),
                changes["is_active"],
            )

            if changes["ip"] != "unassigned" or changes["mask"] != "unassigned":

                if not networking.net.validate_ip(changes["ip"]):
                    raise Exception(f"The given ip {changes['ip']} is invalid.")

                if not networking.net.validate_ip(changes["mask"]):
                    raise Exception(f"The given mask {changes['mask']} is invalid.")

                networking.change_interface(
                    interface["router_id"],
                    networking.net.translate_to_router(interface["name"]),
                    changes["ip"],
                    changes["mask"],
                )
        except TIMEOUT:
            print("Disconnected")

        intf.modify(
            app.session,
            interface,
            ip=changes["ip"],
            mask=changes["mask"],
            is_active=changes["is_active"],
        )

        app.routes = routing.build_routing(app.session)

        return jsonify({"message": "ok"})

    except Exception as e:
        return jsonify({"message": str(e)}), 500


def create_user(db, router, user):
    try:
        if usr.get(db, {"router_id": router, "name": user["name"]}) is not None:
            raise Exception(f"This user {user['name']} already exists")

        networking.add_user(router, user["name"], user["password"])
        usr.add(app.session, router, user)

        return jsonify({"message": "ok"})
    except Exception as e:
        return jsonify({"message": str(e)}), 500


def delete_user(db, router, user):
    try:
        if usr.get(db, {"router_id": router, "name": user["name"]}) is None:
            raise Exception(f"This user {user['name']} doesn't exists")

        networking.delete_user(router, user["name"])
        usr.delete(db, {"router_id": router, "name": user["name"]})

        return jsonify({"message": "ok"})
    except Exception as e:
        return jsonify({"message": str(e)}), 500


def modify_user(db, router, user):
    try:
        print(router)

        if user["name"] == "" or user["password"] == "":
            raise Exception("User void or password void")

        if usr.get(db, {"router_id": router, "name": user["name"]}) is None:
            raise Exception(f"This user {user['name']} doesn't exists")

        if usr.get(db, {"router_id": router, "name": user["new_name"]}) is not None:
            raise Exception(f"This new username {user['new_name']} already exists")

        networking.change_user(router, user["name"], user["new_name"], user["password"])
        usr.modify(
            db, {"router_id": router, "name": user["name"]}, name=user["new_name"]
        )

        return jsonify({"message": "ok"})
    except Exception as e:
        return jsonify({"message": str(e)}), 500
