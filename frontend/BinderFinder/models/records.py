from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
)

from sqlalchemy.orm import relationship

from .meta import Base

class SearchRecord(Base):
    __tablename__ = 'searches'
    id = Column(String(50), primary_key=True)
    keywords = Column(String(255), nullable=False)
    pfams = Column(String(255), nullable=False)


