#!/usr/bin/python
import sys
import os

from reactor.app import App
from reactor import logger
from reactor import component
from reactor.models.device import Device
from reactor.models.user import User
from reactor.components.config import Config
from reactor.components.database import Database
from reactor.components.database import Base

from reactor.models.user import User

from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.orm import relationship, backref

DB_DIR = "./db"

class Cache(Base):
    """"""
    __tablename__ = "cache"
 
    id = Column(Integer, primary_key=True)
    module = Column(String)
    key = Column(String)
    value = Column(String)  

if __name__ == '__main__':
    logger.info("DB Install started")
    
    # create db paths
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)
    
    # setup engine
    db = Database()
    
    # create all tables
    Base.metadata.create_all(db.engine)
    
    logger.info("DB Install finished")

    logger.info("Seeding data")

    # create admin user
    user = User(username='admin',password='admin.123',email='admin@example.com')
    user.generate_password_hash("admin.123")
    db.session.add(user)
    db.session.commit()

    logger.info("Seeding data finished")