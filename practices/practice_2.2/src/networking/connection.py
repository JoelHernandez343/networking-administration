from pexpect import pxssh

from networking import shared, net


def create(ip, user):
    session = pxssh.pxssh()

    print(f"Connecting to {ip} ...")

    session.login(ip, user["name"], user["password"], auto_prompt_reset=False)
    session.sendline("term length 0")
    session.expect("#")

    print(f"Connected to {ip}")

    shared.current_device = net.get_hostname(session.before)

    return session
