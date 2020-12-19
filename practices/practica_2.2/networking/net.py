import socket
import struct


def clear_output(before):
    lines = before.decode("UTF-8").replace("\r", "").split("\n")
    return [l for l in lines if l != ""]


def get_hostname(before):
    return clear_output(before)[-1]


def aton(ip):
    return struct.unpack("!L", socket.inet_aton(ip))[0]


def ntoa(ip):
    return socket.inet_ntoa(struct.pack("!L", ip))


def net_from_ip_mask(ip, mask):
    return ntoa(aton(ip) & aton(mask))
