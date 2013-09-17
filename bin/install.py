#!/usr/bin/python
import sys
sys.path.append("../")

from reactor.app import App
from reactor import logger
from reactor import component
from reactor.models.device import Device
from reactor.components.config import Config
from reactor.components.database import Database
from reactor.components.database import Base

from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String

from sqlalchemy.orm import relationship, backref

class Cache(Base):
    """"""
    __tablename__ = "cache"
 
    id = Column(Integer, primary_key=True)
    module = Column(String)
    key = Column(String)
    value = Column(String)  

if __name__ == '__main__':
    
    logger.info("DB Install started")
    db = Database()
    
    Base.metadata.create_all(db.engine)
    logger.info("DB Install finished")