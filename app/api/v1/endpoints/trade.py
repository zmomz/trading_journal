from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.trade import TradeCreate, TradeResponse, TradeUpdate
from app.crud.trade import get_trade, get_trades_by_user, create_trade, update_trade, delete_trade
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
    trades = get_trades_by_user(db, user_id)
    return trades

@router.patch("/trades/{trade_id}", response_model=TradeResponse)
def update_trade_route(trade_id: int, trade_data: TradeUpdate, db: Session = Depends(get_db)):
    trade = update_trade(db, trade_id, trade_data)
    if not trade:
        raise HTTPException(status_code=404, detail="Trade not found")
    return trade

@router.delete("/trades/{trade_id}", response_model=TradeResponse)
def delete_trade_route(trade_id: int, db: Session = Depends(get_db)):
    trade = delete_trade(db, trade_id)
    if not trade:
        raise HTTPException(status_code=404, detail="Trade not found")
    return trade