from networking import net, shared
from networking.shared import username, password, log


def visit_it(source, current):
    session = net.login(current)
    log("Visited")

    if not source is None:
        shared.topology.add_edge(source["name"], shared.hostname)
        log(f"Added edge ({shared.hostname}, {source['name']})")

    if shared.hostname in shared.visited:
        log("Already visited, skipping.")
        return

    shared.visited.append(shared.hostname)

    connections = net.get_connections(session)

    print(net.get_information(session))

    for hop in net.get_next_hops(session, connections):
        if not net.check_conn(session, hop["hop"]):
            log(f"Without connection: {hop['hop']}")
            continue

        shared.pending.append(
            {
                "source": {"ip": hop["source"], "name": shared.hostname},
                "dest": hop["hop"],
            }
        )

    log("Queued hops")

    session.logout()
