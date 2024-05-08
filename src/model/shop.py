from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class Shop(Base):
    __tablename__ = "shops"

    id = Column(Integer, primary_key=True, index=True)
    shop_id = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    name = Column(String)
    cover = Column(String)
    show_official_shop_label = Column(Boolean)
    is_preferred_plus_seller = Column(Boolean)
    is_shopee_verified = Column(Boolean)
    chat_disabled = Column(Boolean)
    rating_star = Column(Float)
    has_decoration = Column(Boolean)
    last_active_time = Column(DateTime)
    vacation = Column(Boolean)
    description = Column(Text)
    shop_created = Column(DateTime)
    insert_date = Column(DateTime)
    follower_count = Column(Integer)
    item_count = Column(Integer)
    response_rate = Column(Integer)
    campaign_hot_deal_discount_min = Column(Integer)
    shop_rating_good = Column(Integer)
    shop_rating_normal = Column(Integer)
    shop_rating_bad = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    products_in_shop_updated_at = Column(DateTime)
    is_lock = Column(Boolean, default=False)
