import net, config, shared

def open_inner_session(session, ip, username, password):
    session.sendline('ssh -l ' + username + ' ' + ip)
    session.expect(':')
    session.sendline(password)
    session.expect('#')

def close_inner_session(session):
    session.sendline('exit')
    session.expect('#')

def config_r1(session, source):

    commands = [
        'conf t', 'ip route 0.0.0.0 0.0.0.0 ' + source
    ]

    config.send_commands(session, commands, exits=1)

    connections = net.get_connections(session)

    return [c for c in connections if net.get_next_hop(c) != source]

def config_r2(session):
    connections = net.get_connections(session)
    config.rip(session, connections)

def config_r3(session):
    connections = net.get_connections(session)
    config.ospf(session, connections)

def config_routers(session, connections, me):
    routes = []

    for hop in net.get_next_hops(session, connections):
        shared.set_name(me)

        if (not net.check_conn(session, hop['hop'])):
            print(shared.name + 'Without connection: ' + hop['hop'])
            continue
        
        open_inner_session(session, hop['hop'], shared.username, shared.password)

        hostname = net.get_hostname(session.before)

        shared.set_name(me, hostname)

        if (hostname == 'R1'):
            routes = config_r1(session, hop['source'])
            for route in routes:
                route['ip'] = hop['hop']

        elif (hostname == 'R2'):
            config_r2(session)
        else:
            config_r3(session)

        close_inner_session(session)
    
    return routes

def config_r4(session):

    me = net.get_hostname(session.before)

    shared.set_name(me)

    connections = net.get_connections(session)

    commands = ['conf t']
    for route in config_routers(session, connections, me):
        commands.append('ip route ' + route['net'] + ' ' + route['mask'] + ' ' + route['ip'])

    shared.set_name(me)

    config.send_commands(session, commands, exits=1)

    config.ospf(session, connections)
    config.rip(session, connections)

    config.redistribuite_ospf(session)
    config.redistribuite_rip(session)




    


    

        

