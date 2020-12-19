from flask import render_template, jsonify
from app import app


@app.route("/vlans/<int:vlan>")
def vlans(vlan=0):
    print(vlan)

    v = {
        "number": 10,
        "name": "VLAN10",
        "net": "192.168.10.0",
        "mask": "255.255.255.0",
        "gateway": "192.168.10.1",
    }

    switches = [
        {
            "ip": "192.168.1.11",
            "interfaces": [
                {"name": "FastEthernet1/6"},
                {"name": "FastEthernet1/7"},
                {"name": "FastEthernet1/8"},
                {"name": "FastEthernet1/9"},
                {"name": "FastEthernet1/10"},
                {"name": "FastEthernet1/11"},
                {"name": "FastEthernet1/12"},
                {"name": "FastEthernet1/13"},
                {"name": "FastEthernet1/14"},
                {"name": "FastEthernet1/15"},
            ],
        },
        {
            "ip": "192.168.1.12",
            "interfaces": [
                {"name": "FastEthernet1/6"},
                {"name": "FastEthernet1/7"},
                {"name": "FastEthernet1/8"},
                {"name": "FastEthernet1/9"},
                {"name": "FastEthernet1/10"},
                {"name": "FastEthernet1/11"},
                {"name": "FastEthernet1/12"},
                {"name": "FastEthernet1/13"},
                {"name": "FastEthernet1/14"},
                {"name": "FastEthernet1/15"},
            ],
        },
    ]

    return render_template("vlan.html", vlan=v, switches=switches)
