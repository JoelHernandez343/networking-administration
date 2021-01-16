from . import common

from .graph import Graph
from .. import ssh, snmp
from ..ssh import tools


def discover(db, user):
    common.topology = Graph()
    common.pending = []
    common.visited = []
    common.lan = 1

    common.pending.append(
        {
            "source": None,
            "dest": tools.get_default_gateway(),
        }
    )

    for device in common.pending:
        print("Visiting to " + device["dest"])
        visit_it(device["source"], device["dest"], db, user)

    common.topology.render()


def visit_it(source, current, db, user):

    session = ssh.connection.create(current, user)
    common.hostname = ssh.common.current_device

    tools.log("Visited")

    if source is not None:
        common.topology.add_edge(
            source["name"],
            common.hostname,
            get_label(source["ip"], source["mask"]),
        )
        tools.log(f"Added edge ({common.hostname}, {source['name']})")

    if common.hostname in common.visited:
        tools.log("Already visited, skipping.")
        return

    common.visited.append(common.hostname)
    connections = ssh.information.get_connections(session)
    sys_info = snmp.information.get_sys_info(current)
    # Aquí va el agregado a la BD

    for hop in ssh.information.get_next_hops(session, connections):
        if not ssh.tools.check_conn(session, hop["hop"]):
            common.topology.add_edge(
                common.hostname,
                f"{get_label(hop['source'], hop['mask'])}",
                "",
            )

            common.lan += 1

            tools.log(f"Without connection: {hop['hop']}")
            continue

        common.pending.append(
            {
                "source": {
                    "ip": hop["source"],
                    "mask": hop["mask"],
                    "name": common.hostname,
                },
                "dest": hop["hop"],
            }
        )

    tools.log("Queued hops")

    session.logout()


def get_label(ip, mask):
    network = tools.net_from_ip_mask(ip, mask)
    prefix = tools.get_prefix(mask)

    return f"{network}/{prefix}"
