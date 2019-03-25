from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime


class Reminders(Base):
    __tablename__ = 'reminders'

    id = Column(Integer, primary_key=True)
    title = Column(String(50))
    description = Column(String(200))
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime, default=datetime.utcnow)
    email = Column(String(50))

    def __init__(self, title=None, description=None, start_time=None, end_time=None, email=None):
        self.title = title
        self.description = description
        self.start_time = start_time
        self.end_time = end_time
        self.email = email

    def __repr__(self):
        return '<Reminders %r>' % self.reminders