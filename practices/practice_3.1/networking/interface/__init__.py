import time
import threading

from sqlalchemy.orm import scoped_session

from ..snmp import information

from database import SessionLocal
from database.manage import interface as it, router as rt, register as rg


def tracking(thread, interface):
    print(f"[Thread {threading.currentThread().getName()}] Tracking {interface}")

    db = scoped_session(SessionLocal)
    i = it.get(db, interface)
    r = rt.get(db, interface["router_id"])

    while not thread.stopped():
        rg.add(
            db, interface, information.get_if_inout(r["accesible_ip"], i["mib_index"])
        )

        for second in range(30):
            if thread.stopped():
                break
            time.sleep(1)

    print(f"[Thread {threading.currentThread().getName()}] Finished!")

    db.remove()
