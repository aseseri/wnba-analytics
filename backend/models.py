# backend/models.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Player(Base):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    team = Column(String, index=True)
    stats = relationship("PlayerStat", back_populates="player", cascade="all, delete-orphan") # if you delete a player, all of their associated stats will be automatically deleted too

class PlayerStat(Base):
    __tablename__ = "player_stats"
    id = Column(Integer, primary_key=True, index=True)
    season = Column(String, index=True)
    points_per_game = Column(Integer)
    rebounds_per_game = Column(Integer)
    assists_per_game = Column(Integer)
    player_id = Column(Integer, ForeignKey("players.id"))
    player = relationship("Player", back_populates="stats")