import json

from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String

from database import Base

class Feed(Base):
    __tablename__ = 'feed'
    id = Column(Integer, primary_key=True)
    name = Column(String(140), nullable=False)
    lat = Column(String(20), nullable=False)
    lng = Column(String(20), nullable=False)
    address = Column(String(140), nullable=False)
    created_at = Column(DateTime)
    last_modified = Column(DateTime)
    state = Column(String(7))
    description = Column(String(200))

    def __init__(self, name, lat, lng, address, created_at=datetime.now(),
                 last_modified=datetime.now(), state='open',
                 description=None):
        self.name = name
        self.lat = lat
        self.lng = lng
        self.address = address
        self.created_at = created_at
        self.last_modified = last_modified
        self.state = state
        self.description = description

    def __repr__(self):
        return '(name: %r, address: %r, lat: %r, lng: %r, state: %r,'\
        'created_at: %r, last_modified: %r, description: %r)'\
        % (self.name, self.address, self.lat, self.lng, self.state, 
           self.created_at, self.last_modified, self.description)

    @property
    def serialize(self):
        return json.dumps({
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'lat': self.lat,
            'lng': self.lng,
            'state': self.state,
            'created_at': self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            'last_modified': self.last_modified.strftime("%Y-%m-%d %H:%M:%S"),
            'description': self.description
        })
