def status(status):

    status = int(str(status))

    if status == 1:
        return "up"
    if status == 2:
        return "down"
    if status == 3:
        return "testing"

    return "unknown"


def mac(raw_str):
    return ":".join("{:02x}".format(ord(c)) for c in raw_str)
