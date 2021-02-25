from . import configuration
from . import connection
from . import tools


def get_connections(session):
    configuration.send_commands(session, ["sh run | inc interface | ip address | shu"])

    lines = tools.clear_output(session.before)
    lines.pop(0)
    lines.pop()

    table = []

    interface = {}
    active = False

    for line in lines:

        fields = line.strip().split()

        if fields[0] == "interface":
            if active:
                table.append(interface)

            if fields[1] == "Loopback0":
                continue

            interface = {}
            active = True

            interface["name"] = fields[1]

        elif fields[0] == "ip":
            interface["ip"] = fields[2]
            interface["net"] = tools.net_from_ip_mask(fields[2], fields[3])
            interface["mask"] = fields[3]

        elif fields[0] == "shutdown":
            active = False

    return table


def get_next_hops(session, connections):
    hops = []

    for conn in connections:
        hop = tools.get_next_hop(conn)
        hops.append({"source": conn["ip"], "hop": hop, "mask": conn["mask"]})

    return hops


def get_all_connections(session):
    configuration.send_commands(session, ["sh run | inc interface | ip address | shu"])

    lines = tools.clear_output(session.before)
    lines.pop(0)
    lines.pop()

    table = []

    interface = None

    for line in lines:

        fields = line.strip().split()

        if fields[0] == "interface":
            if interface is not None:
                table.append(interface)

            interface = {
                "name": tools.translate_to_flask(fields[1]),
                "ip": "unassigned",
                "mask": "unassigned",
                "net": "unassigned",
                "is_active": True,
            }
        elif fields[0] == "ip":
            interface["ip"] = fields[2]
            interface["net"] = tools.net_from_ip_mask(fields[2], fields[3])
            interface["mask"] = fields[3]

        elif fields[0] == "shutdown":
            interface["is_active"] = False

    table.append(interface)

    return table


def check_next_connection(interface, user):
    session = connection.create(interface["ip"], user)

    next_hop = tools.get_next_hop({"ip": interface["ip"], "net": interface["net"]})

    res = None
    if tools.check_conn(session, next_hop):
        res = next_hop

    session.close()
    return res
