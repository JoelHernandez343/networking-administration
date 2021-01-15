from networking.snmp import snmp_query, oids

community = "ro_4CM1"


def get_sys_info(ip):
    info = {}

    info["sysDescr"] = snmp_query(ip, community, oids.DESCR_OID)
    info["sysContact"] = snmp_query(ip, community, oids.CONTACT_OID)
    info["sysName"] = snmp_query(ip, community, oids.HOSTNAME_OID)
    info["sysLocation"] = snmp_query(ip, community, oids.LOCATION_OID)
    info["hostname"] = info["sysName"].split(".")[0]

    return info
