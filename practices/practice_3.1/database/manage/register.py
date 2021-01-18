from .. import models


def get_all(db, interface_id):
    print(interface_id)

    interface = db.query(models.Interface).get(interface_id)

    if interface is None:
        return []

    return [r.to_dict() for r in interface.registers]
