import subprocess
import socket
import struct
from pexpect import pxssh

from networking import configuration, shared


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


def get_hostname(before):
    return clear_output(before)[-1]


def check_conn(session, ip):
    configuration.send_commands(session, ["ping " + ip + " r 3"])

    output = clear_output(session.before)[-2]
    percentage = output.split()[3]

    return 0 < int(percentage)


def aton(ip):
    return struct.unpack("!L", socket.inet_aton(ip))[0]


def ntoa(ip):
    return socket.inet_ntoa(struct.pack("!L", ip))


def net_from_ip_mask(ip, mask):
    return ntoa(aton(ip) & aton(mask))


def get_wildcard(mask):
    return ntoa(0xFFFFFFFF & ~aton(mask))


def get_broadcast(network, mask):
    net = aton(net_from_ip_mask(network, mask))
    wildcard = aton(get_wildcard(mask))

    return ntoa(net + wildcard)


def check_range_from_network(ip_add, network, mask):
    net = aton(network)
    broadcast = aton(get_broadcast(network, mask))
    ip = aton(ip_add)

    return ip > net and ip < broadcast


def get_connections(session):
    configuration.send_commands(session, ["sh run | inc interface | ip address | shu"])

    lines = clear_output(session.before)
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
            interface["net"] = net_from_ip_mask(fields[2], fields[3])
            interface["mask"] = fields[3]

        elif fields[0] == "shutdown":
            active = False

    return table


def get_next_hop(fields):
    ip = aton(fields["ip"])
    net = aton(fields["net"])

    if net + 1 == ip:
        return ntoa(ip + 1)
    else:
        return ntoa(ip - 1)


def get_next_hops(session, connections):
    hops = []

    for conn in connections:
        hop = get_next_hop(conn)
        hops.append({"source": conn["ip"], "hop": hop})

    return hops


def login(ip):
    session = pxssh.pxssh()
    session.login(ip, shared.username, shared.password, auto_prompt_reset=False)

    session.sendline("term length 0")
    session.expect("#")

    shared.hostname = get_hostname(session.before)

    return session


def get_users(session):
    configuration.send_commands(session, ["sh run | i user"])
    lines = clear_output(session.before)
    lines.pop(0)
    lines.pop()

    users = []
    for line in lines:
        fields = line.strip().split()

        if fields[0] == "username":
            users.append(fields[1])

    return users


def check_user(session, user):
    users = get_users(session)

    return user in users


def get_information(session):
    configuration.send_commands(
        session, ["show version | include Software | processor"]
    )
    lines = clear_output(session.before)
    lines.pop(0)
    lines.pop()

    return (lines[0], lines[1])


def check_interface(session, interface):
    connections = get_connections(session)

    for conn in connections:
        if conn["name"] == interface:
            return conn

    return None


def get_all_interfaces(session):
    configuration.send_commands(session, ["sh ip int br"])
    lines = clear_output(session.before)
    lines.pop(0)
    lines.pop()

    interfaces = []
    for line in lines:
        fields = line.strip().split()

        if fields[0] != "Interface":
            interfaces.append(fields[0])

    return interfaces
