# packet definition
import datetime
import uuid
import collections
import threading
from reactor import component

class Cache(collections.MutableMapping):
    
    def __init__(self, module):
        self.lock = threading.Lock()
        self.module = module
        self.store = {}
        self.engine = component.get("Database").engine
        
        self.load()
        
        
    def load(self):
        result = self.engine.execute("select * from cache where module = ?", self.module)
        
        for row in result:
            key = row["key"]
            value = row["value"]
            self.store[key] = value
            
    def __getitem__(self, key):
        self.lock.acquire()
        try:
            value = self.store[key]
        finally:
            self.lock.release()
        return value

    def __setitem__(self, key, value):
        self.lock.acquire()
        try:
            if(key in self.store):
                self.engine.execute("update cache set value = ? where key = ? and module = ?", value, key, self.module)
            else:
                self.engine.execute("insert into cache (module, key, value) values (?,?,?)", self.module, key, value)
            self.store[key] = value    
        finally:
            self.lock.release()

    def __delitem__(self, key):
        self.lock.acquire()
        try:
            self.engine.execute("delete from cache where module = ? and key = ?", self.module, key)
            del self.store[key]
        finally:
            self.lock.release()
            
    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)
