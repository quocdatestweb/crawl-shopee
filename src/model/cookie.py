from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class Cookie(Base):
    __tablename__ = 'cookies'

    id = Column(Integer, primary_key=True, index=True)
    value = Column(String, nullable=False)
    type = Column(String, nullable=False)
    expired = Column(Boolean, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now())