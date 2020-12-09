from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from database.database import Base


class DictMixIn:
    def to_dict(self):
        return {
            column.name: getattr(self, column.name) for column in self.__table__.columns
        }


class Router(Base, DictMixIn):
    __tablename__ = "Routers"

    ip_max = Column(String, primary_key=True, index=True)
    hostname = Column(String)
    brand = Column(String)
    os = Column(String)

    interfaces = relationship("Interface", backref="Router", lazy="dynamic")
    users = relationship("User", backref="Router", lazy="dynamic")


class Interface(Base, DictMixIn):
    __tablename__ = "Interfaces"

    router_id = Column(
        String, ForeignKey("Routers.ip_max"), primary_key=True, index=True
    )
    name = Column(String, primary_key=True, index=True)
    ip = Column(String)
    net = Column(String)
    mask = Column(String)
    is_active = Column(Boolean)

    router = relationship("Router", backref="Interface")


class User(Base, DictMixIn):
    __tablename__ = "Users"

    router_id = Column(
        String, ForeignKey("Routers.ip_max"), primary_key=True, index=True
    )
    name = Column(String, primary_key=True, index=True)
    password = Column(String)

    router = relationship("Router", backref="User")
