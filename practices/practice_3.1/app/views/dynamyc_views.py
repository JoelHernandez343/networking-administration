from flask import render_template, jsonify, redirect, url_for
from .. import app

from database.manage import router as rt, interface as it


@app.route("/routers/<router>")
def routers(router=""):
    if app.user is None or app.password is None:
        return redirect(url_for("login"))

    r = rt.get(app.session, router)

    if r is None:
        return (
            render_template("404.html", e=f"This router {router} doesn't exits"),
            404,
        )

    return render_template("router.html", router=r)


@app.route("/routers/<router>/<interface>")
def interface(router="", interface=""):
    if app.user is None or app.password is None:
        return redirect(url_for("login"))

    i = it.get(app.session, {"router_id": router, "name": interface})

    if i is None:
        return (
            render_template(
                "404.html", e=f"This interface {interface} of {router} doesn't exits"
            ),
            404,
        )

    return render_template("interface.html", interface=i)
