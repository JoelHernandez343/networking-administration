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
            render_template("404.html", e=f"This vlan {router} doesn't exits"),
            404,
        )

    return render_template("router.html", router=r)
