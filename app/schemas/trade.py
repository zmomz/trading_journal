from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class TradeBase(BaseModel):
    asset_symbol: str
    market: str
    currency: str
    trade_type: str  # Buy/Sell, Short/Long
    entry_price: float
    position_size: float
    leverage: Optional[float] = None
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    commission: Optional[float] = 0.0
    fees: Optional[float] = 0.0

class TradeCreate(TradeBase):
    pass

class TradeResponse(TradeBase):
    id: int
    user_id: int
    executed_at: datetime
    exit_price: Optional[float] = None
    closed_at: Optional[datetime] = None
    is_closed: bool

    model_config = ConfigDict(from_attributes=True)

class TradeUpdate(BaseModel):
    asset_symbol: Optional[str] = None
    market: Optional[str] = None
    currency: Optional[str] = None
    trade_type: Optional[str] = None
    entry_price: Optional[float] = None
    exit_price: Optional[float] = None
    position_size: Optional[float] = None
    leverage: Optional[float] = None
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    commission: Optional[float] = None
    fees: Optional[float] = None
    closed_at: Optional[datetime] = None
