from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.trade import TradeCreate, TradeResponse
from app.crud.trade import get_trade, get_trades_by_user, create_trade
from typing import List

router = APIRouter(prefix="/trades", tags=["Trades"])

@router.post("/", response_model=TradeResponse)
def create_new_trade(trade: TradeCreate, user_id: int, db: Session = Depends(get_db)):
    return create_trade(db, trade, user_id)

@router.get("/{trade_id}", response_model=TradeResponse)
def read_trade(trade_id: int, db: Session = Depends(get_db)):
    db_trade = get_trade(db, trade_id)
    if db_trade is None:
        raise HTTPException(status_code=404, detail="Trade not found")
    return db_trade

@router.get("/user/{user_id}", response_model=List[TradeResponse])
def read_user_trades(user_id: int, db: Session = Depends(get_db)):
    return get_trades_by_user(db, user_id)
