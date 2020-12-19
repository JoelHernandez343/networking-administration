import json

import networking

user = {"name": "cisco", "password": "cisco"}

vlan10 = {
    "name": "VLAN10",
    "number": 10,
    "gateway": "192.168.10.1",
    "mask": "255.255.255.0",
    "interfaces": [
        {
            "switch": "192.168.1.11",
            "name": "FastEthernet1/4",
        },
        {
            "switch": "192.168.1.12",
            "name": "FastEthernet1/15",
        },
    ],
}

vlan20 = {
    "name": "VLAN20",
    "number": 20,
    "gateway": "192.168.20.1",
    "mask": "255.255.255.0",
    "interfaces": [
        {
            "switch": "192.168.1.13",
            "name": "FastEthernet1/15",
        }
    ],
}

vlan30 = {
    "name": "VLAN30",
    "number": 30,
    "gateway": "192.168.30.1",
    "mask": "255.255.255.0",
    "interfaces": [
        {
            "switch": "192.168.1.11",
            "name": "FastEthernet1/15",
        }
    ],
}

networking.set_vlan(vlan10, user, delete=False)
networking.set_vlan(vlan20, user, delete=False)
networking.set_vlan(vlan30, user, delete=False)
# table = networking.get_vlans(user)
# print(json.dumps(table, indent=2))
