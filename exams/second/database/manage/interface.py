from networking import net

from database import models
from database.manage import router


def get(db, int_id):
    interface = db.query(models.Interface).get(int_id)

    return interface.to_dict() if interface is not None else None


def get_from(db, router_id):
    r = db.query(models.Router).get(router_id)

    if r is None:
        return []

    interfaces = []
    for interface in r.interfaces:
        interfaces.append(interface.to_dict())

    return interfaces


def get_all(db):
    interfaces = db.query(models.Interface).all()

    return [r.to_dict() for r in interfaces]


def create_multiple(router_id, interfaces):
    new_interfaces = []
    for i in interfaces:
        new_interfaces.append(
            models.Interface(
                router_id=router_id,
                name=i["name"],
                ip=i["ip"],
                net=i["net"],
                mask=i["mask"],
                is_active=i["is_active"],
            )
        )

    return new_interfaces


def update_id(db, new_ip_max, r):
    interfaces = []
    for i in r.interfaces:
        i.router_id = new_ip_max
        interfaces.append(i)

    db.add_all(interfaces)
    db.commit()


def modify(db, int_id, ip="", mask="", is_active=""):
    i = db.query(models.Interface).get(int_id)

    if i is None:
        return False

    if ip != "":
        i.ip = ip
    if mask != "":
        i.mask = mask
        i.net = net.net_from_ip_mask(ip, mask)
    if is_active != "":
        i.is_active = is_active

    db.add(i)
    db.commit()

    router.update_id(db, i.router.ip_max)

    return True
