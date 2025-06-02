from sqlalchemy import Column, String, DateTime
from .database import Base

class Job(Base):
    __tablename__ = "jobs"

    id       = Column(String, primary_key=True)
    company  = Column(String, index=True)
    title    = Column(String)
    location = Column(String)
    url      = Column(String)
    posted   = Column(DateTime)
