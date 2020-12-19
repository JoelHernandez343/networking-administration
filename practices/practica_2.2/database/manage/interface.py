from database import models


def get_all(db):
    interfaces = db.query(models.Interface).all()

    return [i.to_dict() for i in interfaces]


def create_multiple(vlan_number, interfaces):
    new_interfaces = []

    for i in interfaces:
        new_interfaces.append(
            models.Interface(
                vlan_number=vlan_number, switch=i["switch"], name=i["name"]
            )
        )

    return new_interfaces
