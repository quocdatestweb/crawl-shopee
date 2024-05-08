from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class ProductTimescale(Base):
    __tablename__ = 'new_product_timescale'

    time = Column(DateTime(timezone=True), primary_key=True)
    product_id = Column(String, primary_key=True)
    stock = Column(Integer)
    sold = Column(Integer)
    historical_sold = Column(Integer)
    liked_count = Column(Integer)
    cmt_count = Column(Integer)
    price = Column(Integer)
    price_min = Column(Integer)
    price_max = Column(Integer)
    price_before_discount = Column(Integer)
    show_discount = Column(Integer)
    raw_discount = Column(Integer)
    rating_star_1 = Column(Integer)
    rating_star_2 = Column(Integer)
    rating_star_3 = Column(Integer)
    rating_star_4 = Column(Integer)
    rating_star_5 = Column(Integer)
