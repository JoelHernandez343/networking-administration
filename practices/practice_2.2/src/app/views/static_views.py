from flask import render_template, jsonify, redirect, url_for
from app import app

from networking import get_vlans
from database.manage import vlan
from database.manage import interface


@app.route("/")
def index():
    if app.user is None or app.password is None:
        return redirect(url_for("login"))

    return render_template("index.html", vlans=vlan.get_all(app.session))


@app.route("/add")
def add_page():
    if app.user is None or app.password is None:
        return redirect(url_for("login"))

    switches = interface.to_switch_structure(interface.get_all(app.session))

    return render_template("add.html", switches=switches)


@app.route("/login")
def login():

    return render_template("login.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", e=e), 404
