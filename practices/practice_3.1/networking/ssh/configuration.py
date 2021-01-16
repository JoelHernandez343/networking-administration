from . import common


def send_commands(session, commands, exits=0):
    for _ in range(0, exits):
        commands.append("exit")

    for command in commands:
        log(command)

        session.sendline(command)
        session.expect("#")


def log(message):
    print(f"[{common.current_device}] {message}")
