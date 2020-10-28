#!/usr/bin/python3

import getpass
from pexpect import pxssh

devices = {
    'iosv-1': {
        'prompt': 'iosv-1#',
        'ip': '172.16.1.20'
    },
    'iosv-2':{
        'prompt': 'iosv-2#',
        'ip': '172.16.1.21'
    }
}
commands = ['term length 0', 'show version', 'show run']
username = input('Username: ')
password = getpass.getpass('Password: ')

for device in devices.keys():
    fileName = device + "outout.txt"
    prompt = devices[device]['prompt']
    child = pxssh.pxssh()
    child.login(devices[device]['ip'], username.strip(), password.strip(), auto_prompt_reset=False)

    with open(fileName, 'wb') as f:
        for command in commands:
            child.sendline(command)
            child.expect(prompt)
            f.write(child.before)

    child.logout()