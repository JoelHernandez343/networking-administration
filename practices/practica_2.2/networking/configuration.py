from networking import shared


def send_commands(session, commands, exits=0):
    for _ in range(0, exits):
        commands.append("exit")

    for command in commands:
        print(f"[{shared.current_device}] {command}")
        session.sendline(command)
        session.expect("#")


def create_vlan(session, vlan):
    commands = ["vlan data", f"vlan {vlan['number']} name {vlan['name']}", "apply"]

    send_commands(session, commands, exits=1)


def delete_vlan(session, vlan):
    commands = ["vlan data", f"no vlan {vlan['number']}", "apply"]

    send_commands(session, commands, exits=1)


def set_vlan_interface(session, interface, vlan):
    commands = [
        "conf t",
        f"int {interface['name']}",
        "sw mode ac",
        f"sw ac vlan {vlan['number']}",
    ]

    send_commands(session, commands, exits=2)


def delete_vlan_interface(session, interface):
    set_vlan_interface(session, interface, {"number": 1})


def create_vlan_router(session, vlan):
    commands = [
        "conf t",
        f"int f 0/0.{vlan['number']}",
        f"encap dot {vlan['number']}",
        f"ip add {vlan['gateway']} {vlan['mask']}",
    ]

    send_commands(session, commands, exits=2)


def delete_vlan_router(session, vlan):
    commands = [
        "conf t",
        f"default int f 0/0.{vlan['number']}",
        f"no int f 0/0.{vlan['number']}",
    ]

    send_commands(session, commands)
