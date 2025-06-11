# backend/models.py
from sqlalchemy import Column, Integer, String
from database import Base

class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    team = Column(String, index=True)