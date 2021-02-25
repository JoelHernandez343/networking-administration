from database import models


def create_multiple(router_id, users):
    new_users = []
    for user in users:
        new_users.append(models.User(router_id=router_id, name=user["name"]))

    return new_users


def get_all(db):
    users = db.query(models.User).all()

    return [u.to_dict() for u in users]


def add(db, router_id, user):
    new_user = models.User(router_id=router_id, name=user["name"])

    db.add(new_user)
    db.commit()


def get(db, user_id):
    user = db.query(models.User).get(user_id)

    return user.to_dict() if user is not None else None


def modify(db, user_id, name=""):
    u = db.query(models.User).get(user_id)

    if u is None:
        return False

    if name != "":
        u.name = name

    db.add(u)
    db.commit()

    return True


def delete(db, user_id):
    user = db.query(models.User).get(user_id)

    if user is None:
        return False

    db.delete(user)
    db.commit()

    return True
