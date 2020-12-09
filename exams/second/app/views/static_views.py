from flask import render_template
from app import app


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/topology")
def topology():
    return "This is the topology page"


@app.route("/about")
def about():
    return "This is the about page"