import json

from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, Float, String

from database import Base

class Feed(Base):
    __tablename__ = 'feed'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    lat = Column(Float)
    long = Column(Float)
    timestamp = Column(DateTime)
    tag = Column(String(4))

    def __init__(self, name=None, lat=None, long=None, 
                 timestamp=datetime.now(), tag='sos'):
        self.name = name
        self.lat = lat
        self.long = long
        self.timestamp = timestamp
        self.tag = tag

    def __repr__(self):
        return '(Feed name: %r, lat: %r, long: %r, tag: %r, timestamp: %r)'\
        % (self.name, self.lat, self.long, self.tag, self.timestamp)

    @property
    def serialize(self):
        return json.dumps({
            'id': self.id,
            'name': self.name,
            'lat': self.lat,
            'long': self.long,
            'tag': self.tag,
            'timestamp': self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        })
