from networking import net as network

from database import models
from database.manage import interface


def get_all(db):
    vlans = db.query(models.Vlan).all()

    return [get(db, v.to_dict()["number"]) for v in vlans]


def get(db, vlan_number):
    vlan = db.query(models.Vlan).get(vlan_number)

    if vlan is None:
        return None

    vlan_dict = vlan.to_dict()
    vlan_dict["interfaces"] = [i.to_dict() for i in vlan.interfaces]

    return vlan_dict


def add(db, vlan):
    v = models.Vlan(
        number=vlan["number"],
        name=vlan["name"],
        gateway=vlan["gateway"],
        mask=vlan["mask"],
        net=vlan["net"],
    )

    db.add(v)

    for i in vlan["interfaces"]:
        interface.update_or_create_vlan(
            db, {"switch": i["switch"], "name": i["name"]}, vlan["number"]
        )

    db.commit()


def delete(db, vlan_number):
    vlan = db.query(models.Vlan).get(vlan_number)

    if vlan is None:
        return False

    for i in vlan.interfaces:
        interface.update_or_create_vlan(db, {"switch": i.switch, "name": i.name}, 1)

    db.delete(vlan)
    db.commit()

    return True


def to_switch_structure(vlan):

    if len(vlan["interfaces"]) == 0:
        return []

    interfaces = sorted(vlan["interfaces"], key=lambda x: x["switch"])

    switches = [{"ip": interfaces[0]["switch"], "interfaces": []}]
    index = 0
    for i in interfaces:
        if switches[index]["ip"] != i["switch"]:
            switches.append({"ip": i["switch"], "interfaces": []})
            index += 1

        switches[index]["interfaces"].append(
            {"name": i["name"], "vlan": vlan["number"]}
        )

    return switches
