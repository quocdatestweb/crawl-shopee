from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    local_id = Column(String, nullable=False)
    local_name = Column(String)
    global_id = Column(String, nullable=False, unique=True)
    global_name = Column(String)
    parent_id = Column(String, ForeignKey('categories.global_id'))

    children = relationship('Category', backref='parent', remote_side=[global_id])