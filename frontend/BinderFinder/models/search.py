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

class TempSearch(Base):
    __tablename__ = 'temp'
    __table_args__ = {'prefixes': ['TEMPORARY']}

    patID = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    abstract = Column(String)
    creator = Column(Integer)

