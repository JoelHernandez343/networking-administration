from flask import render_template
from app import app


@app.route("/")
def index():
    return render_template("index.html", routes=app.routes)


@app.route("/topology")
def topology():
    return render_template("topology.html", routes=app.routes)


@app.route("/about")
def about():
    return render_template("about.html", routes=app.routes)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", routes=app.routes, e=e), 404
