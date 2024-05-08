from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class ProductFilter(Base):
    __tablename__ = 'product_filters'

    item_id = Column(String, primary_key=True)
    shop_id = Column(String)
    catid = Column(Integer)
    brand = Column(String)
    shop_location = Column(String)
    lowest_category_id = Column(Integer)