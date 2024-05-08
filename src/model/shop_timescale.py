from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class ShopTimescale(Base):
    __tablename__ = 'shop_timescale'

    time = Column(DateTime(timezone=True), primary_key=True)
    shop_id = Column(String, primary_key=True)
    rating_star = Column(Integer)
    follower_count = Column(Integer)
    item_count = Column(Integer)
    response_rate = Column(Integer)
    campaign_hot_deal_discount_min = Column(Integer)
    shop_rating_good = Column(Integer)
    shop_rating_normal = Column(Integer)
    shop_rating_bad = Column(Integer)
    
