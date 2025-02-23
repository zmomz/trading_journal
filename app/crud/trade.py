from sqlalchemy.orm import Session
from app.models.trade import Trade
from app.schemas.trade import TradeCreate, TradeUpdate
from datetime import datetime

def get_trade(db: Session, trade_id: int):
    return db.query(Trade).filter(Trade.id == trade_id).first()

def get_trades_by_user(db: Session, user_id: int):
    return db.query(Trade).filter(Trade.user_id == user_id, Trade.is_deleted == False).all()

def create_trade(db: Session, trade: TradeCreate, user_id: int):
    db_trade = Trade(
        user_id=user_id,
        asset_symbol=trade.asset_symbol,
        market=trade.market,
        currency=trade.currency,
        trade_type=trade.trade_type,
        entry_price=trade.entry_price,
        position_size=trade.position_size,
        leverage=trade.leverage,
        stop_loss=trade.stop_loss,
        take_profit=trade.take_profit,
        commission=trade.commission,
        fees=trade.fees,
        executed_at=datetime.utcnow(),
        is_closed=False
    )
    db.add(db_trade)
    db.commit()
    db.refresh(db_trade)
    return db_trade

def update_trade(db: Session, trade_id: int, trade_data: TradeUpdate):
    trade = db.query(Trade).filter(Trade.id == trade_id).first()
    if not trade:
        return None
    for key, value in trade_data.dict(exclude_unset=True).items():
        setattr(trade, key, value)
    db.commit()
    db.refresh(trade)
    return trade

def delete_trade(db: Session, trade_id: int):
    trade = db.query(Trade).filter(Trade.id == trade_id).first()
    if not trade:
        return None
    trade.is_deleted = True  
    db.commit()
    return trade