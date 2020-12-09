import topology, shared, net

gateway = {
    'ip': net.get_gateway_linux(),
    'hostname': ''
}

print('[Host] Gateway obtained: ' + gateway['ip'])

shared.ssh.append({
    'origin': None, 
    'dest': gateway
})

for ssh in shared.ssh:
    topology.ssh_process(ssh['origin'], ssh['dest'])

shared.topology.render()