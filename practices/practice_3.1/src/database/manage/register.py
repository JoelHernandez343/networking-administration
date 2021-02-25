import time

from .. import models


def _current_milli_time():
    return round(time.time() * 1000)


def get_all(db, interface_id):

    interface = db.query(models.Interface).get(interface_id)

    if interface is None:
        return []

    return [r.to_dict() for r in interface.registers]


def add(db, interface_id, info):
    register = models.Register(
        router_id=interface_id["router_id"],
        interface_id=interface_id["name"],
        date=_current_milli_time(),
        if_inoctets=info["ifInOctets"],
        if_outoctets=info["ifOutOctets"],
        if_inucastpkts=info["ifInUcastPkts"],
        if_outucastpkts=info["ifOutUcastPkts"],
    )

    db.add(register)
    db.commit()
