import pytest
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.trade import Trade
from app.crud.user import create_user, get_user_by_email
from app.crud.trade import create_trade, get_trade
from app.schemas.user import UserCreate
from app.schemas.trade import TradeCreate
from app.core.security import verify_password
from datetime import datetime

def test_create_user(db: Session):
    user_data = UserCreate(username="testuser", email="test@example.com", password="securepassword")
    user = create_user(db, user_data)
    assert user.username == user_data.username
    assert user.email == user_data.email
    assert verify_password("securepassword", user.hashed_password)

def test_get_user_by_email(db: Session):
    email = "test@example.com"
    user = get_user_by_email(db, email)
    assert user is not None
    assert user.email == email

def test_create_trade(db: Session):
    user = get_user_by_email(db, "test@example.com")
    trade_data = TradeCreate(
        asset_symbol="BTC/USD",
        market="crypto",
        currency="USD",
        trade_type="buy",
        entry_price=50000.0,
        position_size=0.1,
        leverage=None,
        stop_loss=49000.0,
        take_profit=52000.0,
        commission=10.0,
        fees=5.0
    )
    trade = create_trade(db, trade_data, user.id)
    assert trade.asset_symbol == trade_data.asset_symbol
    assert trade.market == trade_data.market
    assert trade.currency == trade_data.currency
    assert trade.trade_type == trade_data.trade_type
    assert trade.entry_price == trade_data.entry_price

def test_get_trade(db: Session):
    trade = get_trade(db, 1)  # Assuming first trade
    assert trade is not None
    assert trade.asset_symbol == "BTC/USD"
