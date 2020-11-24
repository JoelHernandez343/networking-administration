#!/usr/bin/python3

import json, pexpect, getpass

with open('routers.json', 'r') as f:
    devices = json.load(f)

with open('commands.txt', 'r') as f:
    commands = [line for line in f.readlines()]

username = input('Username: ')
password = getpass.getpass('Password: ')

for device in devices.keys():
    p = pexpect.spawn('telnet ' + devices[device]['ip'])
    print('Configuring ssh of device ' + device + '@' + devices[device]['ip'])
    p.expect('Username:')
    p.sendline(username)
    p.expect('Password:')
    p.sendline(password)

    # ssh configuration
    prompt = device + '#'
    for command in commands:
        p.expect("#")
        p.sendline(command)

    print('DONE.')