from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ShopFilter(Base):
    __tablename__ = 'shop_filters'

    shop_id = Column(String, primary_key=True)
    username = Column(String, unique=True)
    is_mall = Column(Boolean)