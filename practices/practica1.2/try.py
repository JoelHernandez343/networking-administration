#!/usr/bin/python3

import json, pexpect, getpass

device = 'R1'

commands = open('commands.txt').readlines()

# with open('commands.txt', 'r') as f:
#     commands = [line for line in f.readlines()]

prompt = device + '#'

for command in commands:
    print(prompt + command)

    if command == 'config t\n' or \
       command == 'exit\n' and prompt == device + '(config-line)#':
        prompt = device + '(config)#'
    elif command == 'line vty 0 15\n':
        prompt = device + "(config-line)#"
    elif command == 'exit\n' and prompt == device + '(config)#':
        prompt = device + '#'

print(prompt)