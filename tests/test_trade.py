import pytest
from sqlalchemy.orm import Session
from app.crud.trade import create_trade, get_trade, get_trades_by_user, update_trade, delete_trade
from app.crud.user import create_user  # Ensure a test user exists
from app.schemas.trade import TradeCreate, TradeUpdate
from app.schemas.user import UserCreate  # Needed to create a test user

from app.models.trade import Trade
from app.models.user import User
from app.models.note import TradeNote

@pytest.fixture
def test_db_cleanup(db: Session):
    """Ensure a completely clean database before each test."""
    db.execute("TRUNCATE TABLE trade_notes, trades, users RESTART IDENTITY CASCADE;")
    db.commit()


@pytest.fixture
def test_user(db: Session):
    """Ensure test user is unique and prevent duplicates."""
    existing_user = db.query(User).filter(User.email == "test@example.com").first()
    if existing_user:
        return existing_user  # Return existing user if already created

    user_data = UserCreate(
        username="testuser",
        email="test@example.com",
        password="securepassword"
    )
    return create_user(db, user_data)



@pytest.fixture
def test_trade(db: Session, test_user):
    """Fixture to create a test trade for a test user, ensuring uniqueness."""
    existing_trade = db.query(Trade).filter(Trade.user_id == test_user.id).first()
    if existing_trade:
        return existing_trade  # Return existing trade to prevent duplication
    
    trade_data = TradeCreate(
        asset_symbol="BTC", market="Crypto", currency="USD",
        trade_type="Buy", entry_price=45000, position_size=1.5
    )
    return create_trade(db, trade_data, user_id=test_user.id)


def test_create_trade(db: Session, test_user):
    """Ensure trades are created with a valid user_id"""
    trade_data = TradeCreate(
        asset_symbol="ETH", market="Crypto", currency="USD",
        trade_type="Sell", entry_price=3200, position_size=0.5
    )
    trade = create_trade(db, trade_data, user_id=test_user.id)  # Now passing user_id
    assert trade.id is not None
    assert trade.asset_symbol == "ETH"

def test_get_trade(db: Session, test_trade):
    trade = get_trade(db, test_trade.id)
    assert trade is not None
    assert trade.asset_symbol == "BTC"

def test_get_trades_by_user(db: Session, test_trade):
    trades = get_trades_by_user(db, test_trade.user_id)
    assert len(trades) > 0

def test_update_trade(db: Session, test_trade):
    update_data = TradeUpdate(entry_price=46000)
    updated_trade = update_trade(db, test_trade.id, update_data)
    assert updated_trade.entry_price == 46000

def test_delete_trade(db: Session, test_trade):
    delete_trade(db, test_trade.id)
    deleted_trade = db.query(Trade).filter(Trade.id == test_trade.id).first()
    assert deleted_trade is not None  # It should still exist
    assert deleted_trade.is_deleted == True  # Ensure it's marked as deleted

