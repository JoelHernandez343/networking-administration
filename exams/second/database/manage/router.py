from database import models
from database.manage import interface, user
from networking import net


def _get_max_ip(interfaces):
    ip_max_n = 0
    ip_max = None
    for i in interfaces:
        if not i["is_active"]:
            continue

        if ip_max_n < net.aton(i["ip"]):
            ip_max_n = net.aton(i["ip"])
            ip_max = i["ip"]

    return ip_max


def get_all(db):
    routers = db.query(models.Router).all()

    return [get(db, r.to_dict()["ip_max"]) for r in routers]


def get(db, router_id):
    router = db.query(models.Router).get(router_id)

    if router is None:
        return None

    router_dict = router.to_dict()
    router_dict["interfaces"] = interface.get_from(db, router_id)
    router_dict["active_interfaces"] = len(
        [i for i in router.interfaces if i.is_active]
    )
    router_dict["users"] = [u.to_dict() for u in router.users]

    return router_dict


def add_w_interfaces_n_users(db, router, interfaces, users):
    ip_max = _get_max_ip(interfaces)

    r = models.Router(
        ip_max=ip_max,
        hostname=router["name"],
        brand=router["brand"],
        os=router["os"],
    )

    db.add(r)
    db.add_all(interface.create_multiple(ip_max, interfaces))
    db.add_all(user.create_multiple(ip_max, users))
    db.commit()


def update_id(db, router_id):
    r = db.query(models.Router).get(router_id)

    new_ip_max = _get_max_ip([i.to_dict() for i in r.interfaces])

    if r is None:
        return False

    interface.update_id(db, new_ip_max, r)

    r.ip_max = new_ip_max

    db.add(r)
    db.commit()


def modify(db, router_id, hostname=""):
    r = db.query(models.Router).get(router_id)

    if r is None:
        return False

    if hostname != "":
        r.hostname = hostname

    db.add(r)
    db.commit()

    return True


def delete(db, router_id):
    router = db.query(models.Router).get(router_id)

    if router is None:
        return False

    for i in router.interfaces:
        db.delete(i)

    for u in router.users:
        db.delete(u)

    db.delete(router)
    db.commit()

    return True
