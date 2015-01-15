#from web import db
import json

#region SqlAlchemy Tools


from sqlalchemy import inspect
from sqlalchemy.orm.state import InstanceState



def get_entity_propnames(entity):
    """ Get entity property names
        :param entity: Entity
        :type entity: sqlalchemy.ext.declarative.api.DeclarativeMeta
        :returns: Set of entity property names
        :rtype: set
    """
    ins = entity if isinstance(entity, InstanceState) else inspect(entity)
    return set(
        ins.mapper.column_attrs.keys() +  # Columns
        ins.mapper.relationships.keys()  # Relationships
    )


def get_entity_loaded_propnames(entity):
    """ Get entity property names that are loaded (e.g. won't produce new queries)
        :param entity: Entity
        :type entity: sqlalchemy.ext.declarative.api.DeclarativeMeta
        :returns: Set of entity property names
        :rtype: set
    """
    ins = inspect(entity)
    keynames = get_entity_propnames(ins)

    # If the entity is not transient -- exclude unloaded keys
    # Transient entities won't load these anyway, so it's safe to include all columns and get defaults
    if not ins.transient:
        keynames -= ins.unloaded

    # If the entity is expired -- reload expired attributes as well
    # Expired attributes are usually unloaded as well!
    if ins.expired:
        keynames |= ins.expired_attributes

    # Finish
    return keynames

class CRUDMixin(object):
    _repr_hide = ['created_at', 'updated_at']
 
    @classmethod
    def query(cls):
        return db.session.query(cls)
 
    @classmethod
    def get(cls, id):
        return db.session.query(cls).get(id)
 
    @classmethod
    def get_by(cls, **kw):
        return db.session.query(cls).filter_by(**kw).first()
 
    @classmethod
    def get_or_404(cls, id):
        rv = db.session.query(cls).get(id)
        if rv is None:
            abort(404)
        return rv
 
    @classmethod
    def get_or_create(cls, **kw):
        r = db.session.query(cls).get_by(**kw)
        if not r:
            r = cls(**kw)
            db.session.add(r)
 
        return r
 
    @classmethod
    def create(cls, **kw):
        r = cls(**kw)
        db.session.add(r)
        return r
 
    def save(self):
        db.session.add(self)
 
    def delete(self):
        db.session.delete(self)
 
    def __repr__(self):
        values = ', '.join("%s=%r" % (n, getattr(self, n)) for n in self.__table__.c.keys() if n not in self._repr_hide)
        return "%s(%s)" % (self.__class__.__name__, values)
 
    def filter_string(self):
        return self.__str__()

    def to_dict(self):
        d = self.__dict__.copy()
        del d['_sa_instance_state']
        return d

    def to_json(self):
        return json.dumps(self.to_dict())


    def __json__(self, exluded_keys=set()):
        return {name: getattr(self, name)
                for name in get_entity_loaded_propnames(self) - exluded_keys}