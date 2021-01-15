from . import snmp_query, convert, oids

community = "ro_4CM1"


def get_sys_info(ip):
    info = {}

    info["sysDescr"] = snmp_query(ip, community, oids.DESCR_OID)
    info["sysContact"] = snmp_query(ip, community, oids.CONTACT_OID)
    info["sysName"] = snmp_query(ip, community, oids.HOSTNAME_OID)
    info["sysLocation"] = snmp_query(ip, community, oids.LOCATION_OID)
    info["hostname"] = info["sysName"].split(".")[0]

    return info


def get_if_inout(ip, n):
    info = {}

    info["ifInOctets"] = snmp_query(ip, community, f"{oids.INTERFACE_OID}.10.{n}")
    info["ifOutOctets"] = snmp_query(ip, community, f"{oids.INTERFACE_OID}.16.{n}")

    info["ifInUcastPkts"] = snmp_query(ip, community, f"{oids.INTERFACE_OID}.11.{n}")
    info["ifOutUcastPkts"] = snmp_query(ip, community, f"{oids.INTERFACE_OID}.17.{n}")

    return info


def get_if_info(ip, n):
    info = {}

    info["ifDescr"] = snmp_query(ip, community, f"{oids.INTERFACE_OID}.2.{n}")
    info["ifMtu"] = snmp_query(ip, community, f"{oids.INTERFACE_OID}.4.{n}")
    info["ifSpeed"] = snmp_query(ip, community, f"{oids.INTERFACE_OID}.5.{n}")
    info["ifPhysAddress"] = convert.mac(
        snmp_query(ip, community, f"{oids.INTERFACE_OID}.6.{n}")
    )
    info["ifAdminSystem"] = convert.status(
        snmp_query(ip, community, f"{oids.INTERFACE_OID}.7.{n}")
    )
    info["ifOperStatus"] = convert.status(
        snmp_query(ip, community, f"{oids.INTERFACE_OID}.8.{n}")
    )

    return info


def get_interfaces(ip):
    interfaces = []

    number = int(snmp_query(ip, community, oids.INTNUMBER_OID)) - 1

    for i in range(number):
        interfaces.append(get_if_info(ip, i + 1))

    return interfaces
