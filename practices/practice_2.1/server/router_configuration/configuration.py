from router_configuration import net, shared


def send_commands(session, commands, exits=0):
    for _ in range(0, exits):
        commands.append("exit")

    for command in commands:
        print(shared.name + command)
        session.sendline(command)
        session.expect("#")


def rip(session, connections):
    commands = ["conf t", "router rip", "version 2", "no auto"]

    for conn in connections:
        commands.append("net " + conn["net"])

    send_commands(session, commands, exits=2)


def ospf(session, connections):
    commands = ["conf t", "router ospf 1"]

    for conn in connections:
        commands.append(
            "net " + conn["net"] + " " + net.get_wildcard(conn["mask"]) + " area 0"
        )

    send_commands(session, commands, exits=2)


def redistribuite_rip(session):
    commands = ["conf t", "router rip", "r ospf 1 metric 10", "r static metric 5"]

    send_commands(session, commands, exits=2)


def redistribuite_ospf(session):
    commands = ["conf t", "router ospf 1", "re rip subnets", "re static subnets"]

    send_commands(session, commands, exits=2)
