from reactor import component
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Database(component.Component):
    def __init__(self):
        component.Component.__init__(self, "Database")
        
        config = component.get("Config")
        engine = config.get('database.engine')
        
        self.engine = create_engine(engine, echo=False)
        self.session = sessionmaker(bind=self.engine)()
        #self.connection = self.engine.connect()
        