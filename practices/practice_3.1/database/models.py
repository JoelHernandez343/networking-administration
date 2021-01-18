from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Boolean,
    ForeignKeyConstraint,
)
from sqlalchemy.orm import relationship

from . import Base


class DictMixIn:
    def to_dict(self):
        return {
            column.name: getattr(self, column.name) for column in self.__table__.columns
        }


class Router(Base, DictMixIn):
    __tablename__ = "Routers"

    ip_max = Column(String, primary_key=True, index=True)
    hostname = Column(String)
    sys_desc = Column(String)
    sys_contact = Column(String)
    sys_name = Column(String)
    sys_location = Column(String)

    accesible_ip = Column(String)

    interfaces = relationship("Interface", backref="Router", lazy="dynamic")


class Interface(Base, DictMixIn):
    __tablename__ = "Interfaces"

    router_id = Column(
        String, ForeignKey("Routers.ip_max"), primary_key=True, index=True
    )
    name = Column(String, primary_key=True, index=True)
    ip = Column(String)
    net = Column(String)
    mask = Column(String)

    if_mtu = Column(String)
    if_speed = Column(String)
    if_physaddress = Column(String)
    if_adminstatus = Column(String)
    if_operstatus = Column(String)
    mib_index = Column(String)

    register_thread_index = Column(Integer)

    router = relationship("Router", backref="Interface")
    registers = relationship("Register", backref="Interface", lazy="dynamic")


class Register(Base, DictMixIn):
    __tablename__ = "Registers"

    router_id = Column(String, primary_key=True, index=True)
    interface_id = Column(String, primary_key=True, index=True)
    date = Column(String, primary_key=True)

    if_inoctets = Column(String)
    if_outoctets = Column(String)
    if_inucastpkts = Column(String)
    if_outucastpkts = Column(String)

    __table_args__ = (
        ForeignKeyConstraint(
            [router_id, interface_id], [Interface.router_id, Interface.name]
        ),
        {},
    )

    interface = relationship(
        "Interface", backref="Register", foreign_keys=[router_id, interface_id]
    )
