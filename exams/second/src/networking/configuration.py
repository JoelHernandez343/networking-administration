from networking import shared, net


def send_commands(session, commands, exits=0):
    for _ in range(0, exits):
        commands.append("exit")

    for command in commands:
        shared.log(command)
        session.sendline(command)
        session.expect("#")


def add_user(session, new_user, new_password):
    commands = ["config t", f"username {new_user} privilege 15 password {new_password}"]
    send_commands(session, commands, exits=1)


def delete_user(session, user):
    commands = [
        "config t",
        f"no username {user}",
    ]
    send_commands(session, commands, exits=1)


def change_user(session, user, new_user, new_password):
    delete_user(session, user)
    add_user(session, new_user, new_password)


def change_hostname(session, new_hostname):
    commands = ["config t", f"hostname {new_hostname}"]
    send_commands(session, commands, exits=1)


def change_interface(session, interface, ip, mask):
    commands = ["config t", f"int {interface}", f"ip add {ip} {mask}"]
    send_commands(session, commands, exits=1)


def toggle_interface(session, interface, on):
    toggle = "no" if on else ""
    commands = ["config t", f"int {interface}", f"{toggle} shutdown"]

    send_commands(session, commands, exits=1)
