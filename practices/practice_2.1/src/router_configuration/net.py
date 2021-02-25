import subprocess, socket, struct
from router_configuration import configuration


def get_default_gateway():
    with open("/proc/net/route") as f:
        for line in f:
            fields = line.strip().split()
            if fields[1] != "00000000" or not int(fields[3], 16) & 2:
                continue

            return socket.inet_ntoa(struct.pack("<L", int(fields[2], 16)))


def ping(ip):
    try:
        subprocess.check_output("ping -c 2 -q " + ip, shell=True)
    except Exception:
        return False
    return True


def clear_output(before):
    return before.decode("UTF-8").replace("\r", "").split("\n")


def check_conn(session, ip):
    configuration.send_commands(session, ["ping " + ip + " r 3"])

    output = clear_output(session.before)[-2]
    percentage = output.split()[3]

    return 0 < int(percentage)


def get_hostname(before):
    return clear_output(before)[-1]


def aton(ip):
    return struct.unpack("!L", socket.inet_aton(ip))[0]


def ntoa(ip):
    return socket.inet_ntoa(struct.pack("!L", ip))


def net_from_ip_mask(ip, mask):
    return ntoa(aton(ip) & aton(mask))


def get_connections(session):
    configuration.send_commands(session, ["sh run | inc interface | ip address"])

    lines = clear_output(session.before)
    lines.pop(0)
    lines.pop()

    table = []

    for line in lines:

        fields = line.strip().split()

        if fields[0] == "ip":
            table.append(
                {
                    "ip": fields[2],
                    "net": net_from_ip_mask(fields[2], fields[3]),
                    "mask": fields[3],
                }
            )

    return table


def get_wildcard(mask):
    return ntoa(0xFFFFFFFF & ~aton(mask))


def get_next_hop(fields):
    ip = aton(fields["ip"])
    net = aton(fields["net"])
    wild = aton(get_wildcard(fields["mask"]))

    if ip == wild + net - 1:
        return ntoa(ip - 1)
    else:
        return ntoa(ip + 1)


def get_next_hops(session, connections):
    hops = []

    for conn in connections:
        hop = get_next_hop(conn)
        hops.append({"source": conn["ip"], "hop": hop})

    return hops