import net, shared
from credentials import password, username, commands
from pexpect import pxssh

def get_hostname(before):
    return before.decode('UTF-8').split('\n')[1]

def get_next_hop(ip, network):
    ip_int = net.ip_to_int(ip)
    network_int = net.ip_to_int(network)

    if ip_int == network_int + 1:
        return net.int_to_ip(network_int + 2)
    else:
        return net.int_to_ip(network_int + 1)

def get_table_route(session, me):
    session.sendline('sh ip ro co')
    session.expect(me['hostname'] + '#')

    return session.before.decode('UTF-8').replace('\r', '')

def get_route_info(session, me):
    table = []
    lines = get_table_route(session, me).split('\n')
    lines.pop(0)
    lines.pop()

    for line in lines:
        if line[0] == 'C':
            fields = line.strip().split()
            table.append({
                'network': fields[1], 
                'interface': fields[5]
            })

    return table

def get_interface_table(session, me):
    session.sendline('sh ip int bri')
    session.expect(me['hostname'] + '#')
    
    return session.before.decode('UTF-8').replace('\r', '')

def get_interface_info(session, me):
    table = []
    lines = get_interface_table(session, me).split('\n')
    lines.pop(0)
    lines.pop()

    for line in lines:
        fields = line.strip().split()
        if fields[0] != 'Interface':
            table.append({
                'interface': fields[0], 
                'ip': fields[1]
            })

    return table

def get_hops(session, origin, me):
    table = []
    
    routes = get_route_info(session, me)
    interfaces = get_interface_info(session, me)

    for route in routes:
        for interface in interfaces:
            if route['interface'] == interface['interface']:
                hop = get_next_hop(interface['ip'], route['network'])

                if (not origin is None and hop == origin['ip']):
                    continue

                table.append({
                    'origin': interface['ip'],
                    'hop': get_next_hop(interface['ip'], route['network'])
                })

    return table


def ssh_process(origin, me):
    # ssh session starts
    session = pxssh.pxssh()
    session.login(me['ip'], username.strip(), password.strip(), auto_prompt_reset=False)
    session.sendline('term length 0')
    session.expect('#')

    # Get the hostname
    me['hostname'] = get_hostname(session.before)
    print('[' + me['hostname'] + '] Visited.')

    # If this connection has a origin, add the edge to the graph
    if not origin is None:
        shared.topology.add_edge(origin['hostname'], me['hostname'])
        print('[' + me['hostname'] + '] Added connection (' + origin['hostname'] + ', ' + me['hostname'] + ')')

    # If this node is already visited, skip
    if me['hostname'] in shared.visited:
        print('[' + me['hostname'] + '] Already visited, skipping hop generation and configuration.')
        session.logout()
        return

    # Add this router to the visited list
    shared.visited.append(me['hostname'])

    # Get the hops and if we can ping them, they are added to the 
    # ssh queue
    for hop in get_hops(session, origin, me):
        if (net.check_conn(hop['hop'])):
            shared.ssh.append({
                'origin': {
                    'ip': hop['origin'],
                    'hostname': me['hostname']
                },
                'dest': {
                    'ip': hop['hop'],
                    'hostname': ''
                }
            })

    print('[' + me['hostname'] + '] Queued hops, configuring ssh user...')

    # Configure the ssh user
    for command in commands:
        session.sendline(command)
        session.expect('#')

    print('[' + me['hostname'] + '] Done.')

    session.logout()