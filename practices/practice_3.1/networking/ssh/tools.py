import socket
import struct

from . import configuration, common


def log(message):
    print(f"[{common.current_device}] {message}")


def clear_output(before):
    lines = before.decode("UTF-8").replace("\r", "").split("\n")
    return [line for line in lines if line != ""]


def aton(ip):
    return struct.unpack("!L", socket.inet_aton(ip))[0]


def ntoa(ip):
    return socket.inet_ntoa(struct.pack("!L", ip))


def net_from_ip_mask(ip, mask):
    return ntoa(aton(ip) & aton(mask))


def get_first_ip(network, mask):
    net = aton(net_from_ip_mask(network, mask))

    return ntoa(net + 1)


def get_hostname(before):
    return clear_output(before)[-1]


def check_conn(session, ip):
    configuration.send_commands(session, ["ping " + ip + " r 3"])

    output = clear_output(session.before)[-2]
    percentage = output.split()[3]

    return 0 < int(percentage)


def get_default_gateway():
    with open("/proc/net/route") as f:
        for line in f:
            fields = line.strip().split()
            if fields[1] != "00000000" or not int(fields[3], 16) & 2:
                continue

            return socket.inet_ntoa(struct.pack("<L", int(fields[2], 16)))


def get_wildcard(mask):
    return ntoa(0xFFFFFFFF & ~aton(mask))


def get_prefix(mask):
    wildcard = aton(get_wildcard(mask))

    counter = 0
    while wildcard != 0:
        counter += 1
        wildcard >>= 1

    return 32 - counter
