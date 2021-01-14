from networking.snmp import snmp_query

community = "ro_4CM1"


def get_sys_info(ip, credentials):
    info = {}

    info["sysDescr"] = snmp_query(ip, community, "1.3.6.1.2.1.1.1.0")
    info["sysContact"] = snmp_query(ip, community, "1.3.6.1.2.1.1.4.0")
    info["sysName"] = snmp_query(ip, community, "1.3.6.1.2.1.1.5.0")
    info["sysLocation"] = snmp_query(ip, community, "1.3.6.1.2.1.1.6.0")

    return info
