from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean
from sqlalchemy.sql import func

Base = declarative_base()

class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    category = Column(String(255))
    click_count = Column(Integer, default=0)
    created_at = Column(TIMESTAMP, server_default=func.now())
    is_active = Column(Boolean, default=True)
