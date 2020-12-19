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
        net=network.net_from_ip_mask(vlan["gateway"], vlan["mask"]),
    )

    db.add(v)
    db.add_all(interface.create_multiple(vlan["number"], vlan["interfaces"]))
    db.commit()


def delete(db, vlan_number):
    vlan = db.query(models.Vlan).get(vlan_number)

    if vlan is None:
        return False

    for i in vlan.interfaces:
        db.delete(i)

    db.delete(vlan)
    db.commit()

    return True
