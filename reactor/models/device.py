from reactor.components.database import Base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.orm import relationship, backref
import json

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
    
    def to_dict(self):
        d = self.__dict__.copy()
        return d
    
    def to_string(self):
        return str(self.to_dict())
    
    def to_json(self):
        return json.dumps(self.to_dict())
    
    def __str__(self):
        return self.to_string()