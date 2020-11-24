username = 'admin'
password = 'admin'
name = ''

def set_name(router0, router1=''):
    global name
    if router1 == '':
        name = '[' + router0 + '] '
    else:
        name = '[' + router0 + '] [' + router1 + '] ' 