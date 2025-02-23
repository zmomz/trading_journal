from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Trade(Base):
    __tablename__ = "trades"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    asset_symbol = Column(String, index=True, nullable=False)
    market = Column(String, nullable=False)
    currency = Column(String, nullable=False)
    trade_type = Column(String, nullable=False)  # Buy/Sell, Short/Long
    entry_price = Column(Float, nullable=False)
    exit_price = Column(Float, nullable=True)  # Null if trade is open
    position_size = Column(Float, nullable=False)
    leverage = Column(Float, nullable=True)
    stop_loss = Column(Float, nullable=True)
    take_profit = Column(Float, nullable=True)
    commission = Column(Float, default=0.0)
    fees = Column(Float, default=0.0)
    executed_at = Column(DateTime, default=datetime.utcnow)
    closed_at = Column(DateTime, nullable=True)
    is_closed = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False) # Soft delete flag

    user = relationship("User", back_populates="trades")
    dca_entries = relationship("DCAEntry", back_populates="trade")
    notes = relationship("TradeNote", back_populates="trade")

class DCAEntry(Base):
    __tablename__ = "dca_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    trade_id = Column(Integer, ForeignKey("trades.id"))
    entry_price = Column(Float, nullable=False)
    position_size = Column(Float, nullable=False)
    executed_at = Column(DateTime, default=datetime.utcnow)
    
    trade = relationship("Trade", back_populates="dca_entries")
