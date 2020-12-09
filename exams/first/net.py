import subprocess, socket, struct

def check_conn(ip):
    try:
        subprocess.check_output("ping -c 2 -q " + ip, shell=True)
    except Exception:
        return False
    return True

def get_gateway_linux():
    with open('/proc/net/route') as f:
        for line in f:
            fields = line.strip().split()
            if fields[1] != '00000000' or not int(fields[3], 16) & 2:
                continue

            return socket.inet_ntoa(struct.pack('<L', int(fields[2], 16)))

def ip_to_int(ip):
    return struct.unpack('!L', socket.inet_aton(ip))[0]

def int_to_ip(ip):
    return socket.inet_ntoa(struct.pack('!L', ip))