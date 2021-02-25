from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from database.database import Base


class DictMixIn:
    def to_dict(self):
        return {
            column.name: getattr(self, column.name) for column in self.__table__.columns
        }


class Vlan(Base, DictMixIn):
    __tablename__ = "Vlans"

    number = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    net = Column(String)
    mask = Column(String)
    gateway = Column(String)

    interfaces = relationship("Interface", backref="Vlan", lazy="dynamic")


class Interface(Base, DictMixIn):
    __tablename__ = "Interfaces"

    vlan_number = Column(Integer, ForeignKey("Vlans.number"), index=True)
    switch = Column(String, primary_key=True, index=True)
    name = Column(String, primary_key=True, index=True)

    vlan = relationship("Vlan", backref="Interface")
