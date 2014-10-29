import os, flask, bcrypt
from reactor.components.database import Base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, DateTime, Integer, String
from sqlalchemy.orm import relationship, backref
from datetime import datetime
from werkzeug.security import safe_str_cmp

from sys import version_info as PYVER
PYVER = PYVER[0]

class User(Base):
    __tablename__ = "users"
    id = Column('id',Integer , primary_key=True)
    username = Column('username', String(20), unique=True , index=True)
    password = Column('password' , String(10))
    email = Column('email',String(50),unique=True , index=True)
    fullname = Column('fullname', String(20), unique=True , index=True)
    created_at = Column('created_at' , DateTime)
    modified_at = Column('modified_at' , DateTime)

 
    def __init__(self , username ,password , email):
        self.username = username
        self.password = password
        self.email = email
        self.created_at = datetime.utcnow()
        self.modified_at = datetime.utcnow()

    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False
 
    def get_id(self):
        return unicode(self.id)

    def generate_password_hash(self, password):
        if not password:
            raise ValueError('Password must be non-empty.')

        if PYVER < 3 and isinstance(password, unicode):
            password = password.encode('u8')
        elif PYVER >= 3 and isinstance(password, bytes):
            password = password.decode('utf-8')
        password = str(password)

        self.password = bcrypt.hashpw(password, bcrypt.gensalt(10))

    def check_password_hash(self, password):
        if PYVER < 3 and isinstance(password, unicode):
            password = password.encode('u8')
        elif PYVER >= 3 and isinstance(password, bytes):
            password = password.decode('utf-8')
        password = str(password)
        return safe_str_cmp(bcrypt.hashpw(password, self.password), self.password)
 
    def __repr__(self):
        return '<User %r>' % (self.username)