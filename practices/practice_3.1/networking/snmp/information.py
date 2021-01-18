from . import convert, oids
from .tools import snmp_query
from ..ssh import tools

community = "ro_4CM1"


def get_sys_info(ip):
    info = {
        "sysDescr": snmp_query(ip, community, oids.DESCR_OID),
        "sysContact": snmp_query(ip, community, oids.CONTACT_OID),
        "sysName": snmp_query(ip, community, oids.HOSTNAME_OID),
        "sysLocation": snmp_query(ip, community, oids.LOCATION_OID),
    }

    info["hostname"] = info["sysName"].split(".")[0]

    return info


def get_if_inout(ip, n):
    return {
        "ifInOctets": snmp_query(ip, community, f"{oids.INTERFACE_OID}.10.{n}"),
        "ifOutOctets": snmp_query(ip, community, f"{oids.INTERFACE_OID}.16.{n}"),
        "ifInUcastPkts": snmp_query(ip, community, f"{oids.INTERFACE_OID}.11.{n}"),
        "ifOutUcastPkts": snmp_query(ip, community, f"{oids.INTERFACE_OID}.17.{n}"),
    }


def get_if_info(ip, n):

    return {
        "ifDescr": tools.translate_to_flask(
            snmp_query(ip, community, f"{oids.INTERFACE_OID}.2.{n}")
        ),
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
        "mibIndex": n,
    }


def get_interfaces(ip):
    interfaces = []

    number = int(snmp_query(ip, community, oids.INTNUMBER_OID)) + 1

    for i in range(number):
        interface = get_if_info(ip, i + 1)

        if interface["ifDescr"] != "Null0" and interface["ifDescr"] != "":
            interfaces.append(interface)

    return interfaces


def check_lost_percentage(interface_source, interface_dest, percentage):

    info_dest = get_if_inout(interface_dest["ip"], interface_dest["mib_index"])
    info_source = get_if_inout(interface_source["ip"], interface_source["mib_index"])

    print(info_dest, info_source)

    lost_packages = int(info_source["ifOutUcastPkts"]) - int(info_dest["ifInUcastPkts"])

    lost_percentage = abs(lost_packages * 100 / int(info_source["ifOutUcastPkts"]))

    print(lost_packages, lost_percentage, percentage, info_source["ifOutUcastPkts"])

    return (lost_percentage >= percentage, lost_percentage)
