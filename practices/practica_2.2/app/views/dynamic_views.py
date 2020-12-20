from flask import render_template, jsonify, redirect, url_for
from app import app

from database.manage import vlan


@app.route("/vlans/<int:vlan_number>")
def vlans(vlan_number=0):
    if app.user is None or app.password is None:
        return redirect(url_for("login"))

    v = vlan.get(app.session, vlan_number)

    if v is None:
        return (
            render_template("404.html", e=f"This vlan {vlan_number} doesn't exits"),
            404,
        )

    switches = vlan.to_switch_structure(v)

    return render_template("vlan.html", vlan=v, switches=switches)
