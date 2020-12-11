from networking import net, shared
from networking.shared import username, password, log

from database import models
from database.manage import router as rt, interface as intf


def set_data_on_db(db, session):
    information = net.get_information(session)
    interfaces = net.get_all_connections(session)
    users = [{"name": u} for u in net.get_users(session)]

    information["name"] = shared.hostname

    rt.add_w_interfaces_n_users(db, information, interfaces, users)


def visit_it(source, current, db):
    session = net.login(current)
    log("Visited")

    if source is not None:
        shared.topology.add_edge(
            source["name"], shared.hostname, get_label(source["ip"], source["mask"])
        )
        log(f"Added edge ({shared.hostname}, {source['name']})")

    if shared.hostname in shared.visited:
        log("Already visited, skipping.")
        return

    shared.visited.append(shared.hostname)
    connections = net.get_connections(session)

    log("Adding router to database")
    set_data_on_db(db, session)

    for hop in net.get_next_hops(session, connections):
        if not net.check_conn(session, hop["hop"]):
            log(f"Without connection: {hop['hop']}")
            continue

        shared.pending.append(
            {
                "source": {
                    "ip": hop["source"],
                    "mask": hop["mask"],
                    "name": shared.hostname,
                },
                "dest": hop["hop"],
            }
        )

    log("Queued hops")

    session.logout()


def get_label(ip, mask):
    network = net.net_from_ip_mask(ip, mask)
    prefix = net.get_prefix(mask)

    return f"{network}/{prefix}"
