import datetime

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    DateTime
)
from sqlalchemy.orm import relationship

from .meta import Base

class Search(Base):
    __tablename__ = 'search'
    patID = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    abstract = Column(String)
    creator = Column(Integer)

class SearchRecord(Base):
    __tablename__ = 'searches'
    id = Column(String(50), primary_key=True)
    keywords = Column(String(255), unique=True, nullable=False)
    user = Column(Integer)
    date = Column(DateTime, default=datetime.datetime.utcnow)
