from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class TradeNoteBase(BaseModel):
    trade_id: int
    reason: Optional[str] = None
    market_condition: Optional[str] = None  # Bullish/Bearish/Sideways
    emotional_state: Optional[str] = None  # Confidence/Fear/Greed
    mistakes_lessons: Optional[str] = None

class TradeNoteCreate(TradeNoteBase):
    pass

class TradeNoteUpdate(BaseModel):
    pass

class TradeNoteResponse(TradeNoteBase):
    id: int
    created_at: datetime
    deleted: bool
    
    model_config = ConfigDict(from_attributes=True)
