from flask import render_template, jsonify, redirect, url_for
from app import app


from database.manage import router


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/")
def index():
    if app.user is None or app.password is None:
        return redirect(url_for("login"))

    return render_template("index.html", routers=router.get_all(app.session))


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", e=e), 404
