from . import convert, oids
from .tools import snmp_query

community = "ro_4CM1"


def get_sys_info(ip):
    return {
        "sysDescr": snmp_query(ip, community, oids.DESCR_OID),
        "sysContact": snmp_query(ip, community, oids.CONTACT_OID),
        "sysName": snmp_query(ip, community, oids.HOSTNAME_OID),
        "sysLocation": snmp_query(ip, community, oids.LOCATION_OID),
    }


def get_if_inout(ip, n):
    return {
        "ifInOctets": snmp_query(ip, community, f"{oids.INTERFACE_OID}.10.{n}"),
        "ifOutOctets": snmp_query(ip, community, f"{oids.INTERFACE_OID}.16.{n}"),
        "ifInUcastPkts": snmp_query(ip, community, f"{oids.INTERFACE_OID}.11.{n}"),
        "ifOutUcastPkts": snmp_query(ip, community, f"{oids.INTERFACE_OID}.17.{n}"),
    }


def get_if_info(ip, n):

    return {
        "ifDescr": snmp_query(ip, community, f"{oids.INTERFACE_OID}.2.{n}"),
        "ifMtu": snmp_query(ip, community, f"{oids.INTERFACE_OID}.4.{n}"),
        "ifSpeed": snmp_query(ip, community, f"{oids.INTERFACE_OID}.5.{n}"),
        "ifPhysAddress": convert.mac(
            snmp_query(ip, community, f"{oids.INTERFACE_OID}.6.{n}")
        ),
        "ifAdminStatus": convert.status(
            snmp_query(ip, community, f"{oids.INTERFACE_OID}.7.{n}")
        ),
        "ifOperStatus": convert.status(
            snmp_query(ip, community, f"{oids.INTERFACE_OID}.8.{n}")
        ),
    }


def get_interfaces(ip):
    interfaces = []

    number = int(snmp_query(ip, community, oids.INTNUMBER_OID)) - 1

    for i in range(number):
        interfaces.append(get_if_info(ip, i + 1))

    return interfaces
