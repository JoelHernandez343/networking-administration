import re

from networking import configuration
from networking import net
from networking import shared


def get_vlans_vtp_server(session):
    commands = ["sh vlan-s br"]

    configuration.send_commands(session, commands)
    lines = net.clear_output(session.before)[3:-1]

    pattern = re.compile("^[0-9]+$")

    vlans = []

    for line in lines:
        fields = line.strip().split()

        if pattern.search(fields[0]):

            vlan_number = int(fields[0])

            if vlan_number > 1001:
                break

            vlan = {}
            vlan["number"] = vlan_number
            vlan["name"] = fields[1]

            vlans.append(vlan)

    return vlans


def get_index_vlan(number, vlans):
    return next((i for (i, d) in enumerate(vlans) if d["number"] == number), None)


def get_vlans_switch(session, switch, vlans):
    commands = ["sh vlan-s br"]

    configuration.send_commands(session, commands)
    lines = net.clear_output(session.before)[3:-1]

    pattern = re.compile("^[0-9]+$")

    current_vlan = None
    interfaces = []

    for line in lines:
        fields = line.strip().split()

        if pattern.search(fields[0]):

            if current_vlan is not None:
                j = get_index_vlan(current_vlan, vlans)

                if "interfaces" not in vlans[j]:
                    vlans[j]["interfaces"] = []

                for i in interfaces:
                    vlans[j]["interfaces"].append(
                        {
                            "switch": switch,
                            "name": i.replace(",", "").replace("Fa", "FastEthernet"),
                        }
                    )

            current_vlan = int(fields[0])

            if not any(v["number"] == current_vlan for v in vlans):
                current_vlan = None
                continue

            interfaces = fields[3:]

        elif current_vlan is not None:
            interfaces += fields

    return vlans


def get_vlans_router(session, vlans):
    commands = ["sh run | i FastEthernet0/0| ip add"]

    configuration.send_commands(session, commands)
    lines = net.clear_output(session.before)[1:-1]

    current_vlan = None

    for line in lines:
        fields = line.strip().split()

        if fields[0] == "interface":

            if fields[1] == "FastEthernet0/0":
                current_vlan = 1
            else:
                current_vlan = int(fields[1].replace("FastEthernet0/0.", ""))

            if not any(v["number"] == current_vlan for v in vlans):
                current_vlan = None
                continue

        elif current_vlan is not None and fields[0] != "no":

            j = get_index_vlan(current_vlan, vlans)

            vlans[j]["gateway"] = fields[2]
            vlans[j]["mask"] = fields[3]
            vlans[j]["net"] = net.net_from_ip_mask(fields[2], fields[3])

    return vlans
