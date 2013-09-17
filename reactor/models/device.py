from reactor.components.database import Base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.orm import relationship, backref

class Device(Base):
    """"""
    __tablename__ = "devices"
    id = Column(Integer, primary_key=True)
    address = Column(String)
    status = Column(String)
    adapter = Column(String) 
    
    def __init__(self):
        self.id = 0
        self.address = None
        self.status = "unknown"
        self.adapter = None
    
    def send(self, message):
        self.adapter.write(message)
    
    def to_dict(self):
        d = self.__dict__.copy()
        return d