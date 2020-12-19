from flask import render_template
from app import app


@app.route("/")
def index():
    vlans = [
        {
            "number": 10,
            "name": "VLAN10",
            "net": "192.168.10.0",
            "mask": "255.255.255.0",
            "gateway": "192.168.10.1",
        },
        {
            "number": 20,
            "name": "VLAN20",
            "net": "192.168.20.0",
            "mask": "255.255.255.0",
            "gateway": "192.168.20.1",
        },
        {
            "number": 30,
            "name": "VLAN30",
            "net": "192.168.30.0",
            "mask": "255.255.255.0",
            "gateway": "192.168.30.1",
        },
    ]

    return render_template("index.html", vlans=vlans)


@app.route("/add")
def add_page():

    switches = [
        {
            "ip": "192.168.1.11",
            "interfaces": [
                {"name": "FastEthernet1/6", "vlan": 1},
                {"name": "FastEthernet1/7", "vlan": 1},
                {"name": "FastEthernet1/8", "vlan": 1},
                {"name": "FastEthernet1/9", "vlan": 10},
                {"name": "FastEthernet1/10", "vlan": 1},
                {"name": "FastEthernet1/11", "vlan": 20},
                {"name": "FastEthernet1/12", "vlan": 1},
                {"name": "FastEthernet1/13", "vlan": 30},
                {"name": "FastEthernet1/14", "vlan": 20},
                {"name": "FastEthernet1/15", "vlan": 10},
            ],
        },
        {
            "ip": "192.168.1.12",
            "interfaces": [
                {"name": "FastEthernet1/6", "vlan": 1},
                {"name": "FastEthernet1/7", "vlan": 1},
                {"name": "FastEthernet1/8", "vlan": 1},
                {"name": "FastEthernet1/9", "vlan": 1},
                {"name": "FastEthernet1/10", "vlan": 1},
                {"name": "FastEthernet1/11", "vlan": 1},
                {"name": "FastEthernet1/12", "vlan": 1},
                {"name": "FastEthernet1/13", "vlan": 1},
                {"name": "FastEthernet1/14", "vlan": 1},
                {"name": "FastEthernet1/15", "vlan": 1},
            ],
        },
    ]

    return render_template("add.html", switches=switches)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", e=e), 404
