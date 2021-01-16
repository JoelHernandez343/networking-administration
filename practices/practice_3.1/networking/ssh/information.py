from . import configuration
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


def get_next_hop(fields):
    ip = tools.aton(fields["ip"])
    net = tools.aton(fields["net"])

    if net + 1 == ip:
        return tools.ntoa(ip + 1)
    else:
        return tools.ntoa(ip - 1)


def get_next_hops(session, connections):
    hops = []

    for conn in connections:
        hop = get_next_hop(conn)
        hops.append({"source": conn["ip"], "hop": hop, "mask": conn["mask"]})

    return hops
