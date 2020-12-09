from flask import render_template
from app import app


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
    return "This is the list of routers"


def render_router(router):
    # Se checa la existencia del router, si no, un 404
    # si existe, devolvemos la template

    return f"This is the router {router}"


def render_interface_router(router, interface):
    return f"This is the interface {interface} of router {router}"
