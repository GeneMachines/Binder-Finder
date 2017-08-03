from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from .meta import Base

class Sequence(Base):
    __tablename__ = 'sequence'
    seqID = Column(String(25), primary_key=True)
    emblID = Column(String(25))
    patID = Column(Integer, nullable=False)
    seq = Column(String, nullable=False)

