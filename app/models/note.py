from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class TradeNote(Base):
    __tablename__ = "trade_notes"
    
    id = Column(Integer, primary_key=True, index=True)
    trade_id = Column(Integer, ForeignKey("trades.id"), nullable=False)
    reason = Column(String, nullable=True)
    market_condition = Column(String, nullable=True)  # Bullish/Bearish/Sideways
    emotional_state = Column(String, nullable=True)  # Confidence/Fear/Greed
    mistakes_lessons = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    deleted = Column(Boolean, default=False)
    
    trade = relationship("Trade", back_populates="notes")
