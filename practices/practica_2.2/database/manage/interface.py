from database import models


def get(db, interface_id):
    interface = db.query(models.Interface).get(interface_id)

    return interface.to_dict()


def get_all(db):
    interfaces = db.query(models.Interface).all()

    return [i.to_dict() for i in interfaces]


def update_or_create_vlan(db, interface_id, new_vlan_number):
    interface = db.query(models.Interface).get(interface_id)

    if interface is None:
        interface = models.Interface(
            switch=interface_id["switch"],
            name=interface_id["name"],
            vlan_number=new_vlan_number,
        )
    else:
        interface.vlan_number = new_vlan_number

    db.add(interface)
    db.commit()

    return True


def create_multiple(vlan_number, interfaces):
    new_interfaces = []

    for i in interfaces:
        new_interfaces.append(
            models.Interface(
                vlan_number=vlan_number, switch=i["switch"], name=i["name"]
            )
        )

    return new_interfaces


def to_switch_structure(interfaces):
    if len(interfaces) == 0:
        return []

    interfaces = sorted(interfaces, key=lambda x: x["switch"])

    switches = [{"ip": interfaces[0]["switch"], "interfaces": []}]
    index = 0
    for i in interfaces:
        if switches[index]["ip"] != i["switch"]:
            switches.append({"ip": i["switch"], "interfaces": []})
            index += 1

        if i["switch"] == "192.168.1.11" and i["name"] == "FastEthernet1/14":
            print("Skipped FastEthernet1/14 of 192.168.1.11")
            continue

        switches[index]["interfaces"].append(
            {"name": i["name"], "vlan": i["vlan_number"]}
        )

    return switches
