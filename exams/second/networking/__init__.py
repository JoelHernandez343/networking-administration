from pexpect.exceptions import TIMEOUT

from networking import visit, shared, net, configuration


def discover_topology(db):
    shared.pending = []
    shared.visited = []

    shared.pending.append({"source": None, "dest": net.get_default_gateway()})

    for device in shared.pending:
        print("Visiting to " + device["dest"])
        visit.visit_it(device["source"], device["dest"], db)

    # shared.topology.render()


def add_user(ip, new_user, new_password):
    session = net.login(ip)
    configuration.add_user(session, new_user, new_password)
    session.logout()


def delete_user(ip, user):
    session = net.login(ip)
    configuration.delete_user(session, user)
    session.logout()


def change_user(ip, user, new_user, new_password):
    session = net.login(ip)

    if not net.check_user(session, user):
        print(f"The user {user} doesn't exists in {ip}")
        session.logout()
        return

    if user != new_user and net.check_conn(session, new_user):
        print(f"The new user {new_user} already exists.")
        session.logout()
        return

    configuration.change_user(session, user, new_user, new_password)

    session.logout()


def change_hostname(ip, new_hostname):
    session = net.login(ip)
    shared.hostname = new_hostname
    configuration.change_hostname(session, new_hostname)
    session.logout()


def change_interface(ip, interface, new_ip, new_mask):
    try:
        session = net.login(ip)

        result = net.check_interface(session, interface)

        if result is None:
            raise Exception(f"The interface {interface} doenst exists in the router.")
            return

        if not net.check_range_from_network(
            new_ip, net.net_from_ip_mask(new_ip, new_mask), new_mask
        ):
            raise Exception(f"The new ip {new_ip} is invalid for new mask {new_mask}")
            return

        configuration.change_interface(session, interface, new_ip, new_mask)

    except TIMEOUT:
        raise


def toggle_interface(ip, interface, on):
    session = net.login(ip)
    session.timeout = 10

    if interface not in net.get_all_interfaces(session):
        raise Exception(f"The interface {interface} does not exists.")
        return

    try:
        configuration.toggle_interface(session, interface, on)
    except TIMEOUT:
        raise
