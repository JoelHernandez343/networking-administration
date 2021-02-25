from networking import configuration
from networking import information as info
from networking import connection


def set_vlan(vlan, user, delete=False):
    vtp_server = "192.168.1.11"

    set_vlan_vtp_server(vlan, user, vtp_server, delete)
    set_vlan_switch(vlan, user, delete)
    set_vlan_router(vlan, user, delete)


def set_vlan_vtp_server(vlan, user, vtp_server, delete):

    session = connection.create(vtp_server, user)

    if not delete:
        configuration.create_vlan(session, vlan)
    else:
        configuration.delete_vlan(session, vlan)


def set_vlan_switch(vlan, user, delete):

    if len(vlan["interfaces"]) == 0:
        return

    interfaces = sorted(vlan["interfaces"], key=lambda x: x["switch"])
    switch = interfaces[0]["switch"]
    session = connection.create(switch, user)

    for i in interfaces:

        if switch != i["switch"]:
            switch = i["switch"]
            session = connection.create(switch, user)

        if not delete:
            configuration.set_vlan_interface(session, i, vlan)
        else:
            configuration.delete_vlan_interface(session, i)


def set_vlan_router(vlan, user, delete):
    session = connection.create("192.168.1.1", user)

    if not delete:
        configuration.create_vlan_router(session, vlan)
    else:
        configuration.delete_vlan_router(session, vlan)


def get_vlans(user):

    vtp_server = "192.168.1.11"
    switches = ["192.168.1.11", "192.168.1.12", "192.168.1.13"]

    session = connection.create(vtp_server, user)
    vlans = info.get_vlans_vtp_server(session)

    for s in switches:
        session = connection.create(s, user)
        vlans = info.get_vlans_switch(session, s, vlans)

    return info.get_vlans_router(connection.create("192.168.1.1", user), vlans)
