import json

from flask import render_template, jsonify, request
from app import app

from database.manage import router as rt, interface as intf, user


@app.route("/routers")
@app.route("/routers/<path:subpath>")
def routers(subpath=""):
    routes = [r for r in subpath.split("/") if r != ""]

    if len(routes) == 0:
        return render_routers()

    elif len(routes) == 1:
        return render_router(routes[0])

    else:
        return render_interface_router(routes[0], routes[1])


def render_routers():
    return render_template(
        "routers.html", routes=app.routes, routers=rt.get_all(app.session)
    )


def render_router(router):
    r = rt.get(app.session, router)

    if r is None:
        return jsonify({"message": f"This router {router} doesnt exist"}), 404

    return render_template("router.html", routes=app.routes, router=r)


def render_interface_router(router, interface):
    print(router, interface)
    i = intf.get(app.session, {"router_id": router, "name": interface})

    if i is None:
        return jsonify({"message": f"This router {router} doesnt exist"}), 404

    return render_template("interface.html", routes=app.routes, interface=i)
