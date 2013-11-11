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

    def __init__(self, name=None, lat=None, long=None, 
                 timestamp=datetime.now()):
        self.name = name
        self.lat = lat
        self.long = long
        self.timestamp = timestamp

    def __repr__(self):
        return 'name: %r, lat: %r, long: %r, timestamp: %r' % (
            self.name, self.lat, self.long, self.timestamp)
