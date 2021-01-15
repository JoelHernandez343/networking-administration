from . import snmp_set, oids

community = "rw_4CM1"


def set_hostname(ip, new_name):
    snmp_set(ip, community, oids.HOSTNAME_OID, new_name)
