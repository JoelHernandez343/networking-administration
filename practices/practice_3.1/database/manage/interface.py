from .. import models


def create_multiple(router_id, interfaces):
    new_interfaces = []

    for i in interfaces:
        new_interfaces.append(
            models.Interface(
                router_id=router_id,
                name=i["name"],
                ip=i["ip"],
                net=i["net"],
                mask=i["mask"],
                if_mtu=i["ifMtu"],
                if_speed=i["ifSpeed"],
                if_physaddress=i["ifPhysAddress"],
                if_adminstatus=i["ifAdminStatus"],
                if_operstatus=i["ifOperStatus"],
                mib_index=i["mibIndex"],
            )
        )

    return new_interfaces


def get(db, int_id):
    interface = db.query(models.Interface).get(int_id)

    return interface.to_dict() if interface is not None else None
