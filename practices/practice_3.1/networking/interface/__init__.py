import time
import threading

from sqlalchemy.orm import scoped_session

from ..snmp import information

from database import SessionLocal, models
from database.manage import interface as it, router as rt


def _current_milli_time():
    return round(time.time() * 1000)


def tracking(thread, interface):
    print(f"[Thread {threading.currentThread().getName()}] Tracking {interface}")

    db = scoped_session(SessionLocal)
    i = it.get(db, interface)
    r = rt.get(db, interface["router_id"])

    while not thread.stopped():
        info = information.get_if_inout(r["accesible_ip"], i["mib_index"])

        register = models.Register(
            router_id=interface["router_id"],
            interface_id=interface["name"],
            date=_current_milli_time(),
            if_inoctets=info["ifInOctets"],
            if_outoctets=info["ifOutOctets"],
            if_inucastpkts=info["ifInUcastPkts"],
            if_outucastpkts=info["ifOutUcastPkts"],
        )

        db.add(register)
        db.commit()

        for second in range(30):
            if thread.stopped():
                break
            time.sleep(1)

    print(f"[Thread {threading.currentThread().getName()}] Finished!")

    db.remove()
