#!/usr/bin/env python3
import router, shared, net
from pexpect import pxssh

shared.username = 'admin'
shared.password = 'admin'

gateway = net.get_default_gateway()

session = pxssh.pxssh()

print('Connecting to ' + gateway + '...')

session.login(gateway, shared.username, shared.password, auto_prompt_reset=False)
session.sendline('term length 0')
session.expect('#')

router.config_r4(session)

session.logout()