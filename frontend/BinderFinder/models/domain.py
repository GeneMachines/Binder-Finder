from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from .meta import Base

class Domain(Base):
    __tablename__ = 'domain'
    domainID = Column(Integer, primary_key=True)
    pfamID = Column(Integer, nullable=True)
    emblID = Column(String(25), nullable=False)


