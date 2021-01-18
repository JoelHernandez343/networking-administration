from .. import models
from . import interface
from networking.ssh import tools


def _get_max_ip(interfaces):
    ip_max_n = 0
    ip_max = None
    for i in interfaces:
        if not i["is_active"]:
            continue

        if ip_max_n < tools.aton(i["ip"]):
            ip_max_n = tools.aton(i["ip"])
            ip_max = i["ip"]

    return ip_max


def get_all(db):
    routers = db.query(models.Router).all()

    res = []
    for router in routers:
        r = router.to_dict()
        r["interfaces"] = [i.to_dict() for i in router.interfaces]

        res.append(r)

    return res


def get(db, router_id):
    router = db.query(models.Router).get(router_id)

    if router is None:
        return None

    res = router.to_dict()
    res["interfaces"] = [i.to_dict() for i in router.interfaces]

    return res


def add(db, router, interfaces):
    ip_max = _get_max_ip(interfaces)

    r = models.Router(
        ip_max=ip_max,
        hostname=router["hostname"],
        sys_desc=router["sysDescr"],
        sys_contact=router["sysContact"],
        sys_name=router["sysName"],
        sys_location=router["sysLocation"],
        accesible_ip=router["accesible_ip"],
    )

    db.add(r)
    db.add_all(interface.create_multiple(ip_max, interfaces))
    db.commit()

    return get(db, ip_max)


def modify(db, router_id, hostname=""):
    router = db.query(models.Router).get(router_id)

    if router is None:
        return False

    if hostname == "":
        raise Exception("Hostname must not be empty")

    router.hostname = hostname

    db.add(router)
    db.commit()

    return True
