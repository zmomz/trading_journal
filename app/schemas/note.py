from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class TradeNoteBase(BaseModel):
    reason: Optional[str] = None
    market_condition: Optional[str] = None  # Bullish/Bearish/Sideways
    emotional_state: Optional[str] = None  # Confidence/Fear/Greed
    mistakes_lessons: Optional[str] = None

class TradeNoteCreate(TradeNoteBase):
    trade_id: int

class TradeNoteResponse(TradeNoteBase):
    id: int
    trade_id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
