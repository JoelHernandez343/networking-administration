import getpass
username = input('Username: ')
password = getpass.getpass('Password: ')
# username = 'admin'
# password = 'firulais'

with open('commands.txt', 'r') as f:
    commands = [line for line in f.readlines()]