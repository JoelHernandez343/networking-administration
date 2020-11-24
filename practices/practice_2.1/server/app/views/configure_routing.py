import time

from flask import render_template, request, jsonify, make_response
from app import app

@app.route('/configure_routing')
def configure_routing():
    return render_template('configure_routing.html')

@app.route('/configure_routing/configure', methods=['POST'])
def configuring():
    req = request.get_json()

    print(req)

    time.sleep(3)

    return make_response(jsonify(req), 200)
