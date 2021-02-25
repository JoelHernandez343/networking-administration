import time, json

from flask import render_template, request, jsonify, make_response
from app import app
from router_configuration import configure


@app.route("/configure_routing")
def configure_routing():
    return render_template("configure_routing.html")


@app.route("/configure_routing/configure", methods=["POST"])
def configuring():
    req = request.get_json()

    print(req)

    try:
        configure()
        return make_response(jsonify(req), 200)
    except Exception as e:
        obj = {"message": str(e)}
        return make_response(json.dumps(obj), 500)
