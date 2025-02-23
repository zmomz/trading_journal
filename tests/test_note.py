import pytest
from sqlalchemy.orm import Session
from app.models.note import TradeNote
from app.models.trade import Trade
from app.models.user import User
from app.crud.note import create_note, get_note, get_notes_by_trade, update_note, soft_delete_note
from app.crud.trade import create_trade
from app.crud.user import create_user
from app.schemas.note import TradeNoteCreate, TradeNoteUpdate
from app.schemas.trade import TradeCreate
from app.schemas.user import UserCreate

@pytest.fixture
def test_db_cleanup(db: Session):
    """Ensure clean database state before each test"""
    db.query(TradeNote).delete()
    db.query(Trade).delete()
    db.query(User).delete()
    db.commit()

@pytest.fixture
def test_user(db: Session, test_db_cleanup):
    """Create a test user"""
    user_data = UserCreate(
        username="testuser",
        email="test@example.com",
        password="securepassword"
    )
    return create_user(db, user_data)

@pytest.fixture
def test_trade(db: Session, test_user):
    """Create a test trade linked to a user"""
    trade_data = TradeCreate(
        asset_symbol="BTC", market="Crypto", currency="USD",
        trade_type="Buy", entry_price=45000, position_size=1.5
    )
    return create_trade(db, trade_data, user_id=test_user.id)

@pytest.fixture
def test_note(db: Session, test_trade):
    """Create a test note linked to a trade"""
    note_data = TradeNoteCreate(trade_id=test_trade.id, reason="Test Note")
    return create_note(db, note_data)

def test_create_note(db: Session, test_trade):
    """Test note creation with valid trade_id"""
    note_data = TradeNoteCreate(trade_id=test_trade.id, reason="First Note")
    note = create_note(db, note_data)
    assert note.id is not None
    assert note.reason == "First Note"

def test_get_note(db: Session, test_note):
    """Test retrieving an existing note"""
    note = get_note(db, test_note.id)
    assert note is not None
    assert note.reason == "Test Note"

def test_get_notes_by_trade(db: Session, test_trade, test_note):
    """Test retrieving all notes for a trade"""
    notes = get_notes_by_trade(db, test_trade.id)
    assert len(notes) > 0
    assert notes[0].reason == "Test Note"

def test_update_note(db: Session, test_trade):
    """Test updating an existing note that is NOT deleted."""
    
    # Step 1: Create a fresh note
    note_data = TradeNoteCreate(trade_id=test_trade.id, reason="Original Note")
    test_note = create_note(db, note_data)

    # Step 2: Ensure update is not empty
    update_data = TradeNoteUpdate(reason="Updated Note")

    # Step 3: Perform update
    updated_note = update_note(db, test_note.id, update_data)

    # Step 4: Retrieve and verify update
    retrieved_note = get_note(db, test_note.id)

    assert updated_note is not None, "Updated note should exist"
    assert retrieved_note is not None, "Retrieved note should exist"
    assert retrieved_note.reason == "Updated Note", f"Expected 'Updated Note', got '{retrieved_note.reason}'"


def test_update_deleted_note(db: Session, test_note):
    """Test that updating a deleted note does NOT work"""
    soft_delete_note(db, test_note.id)  # Soft delete the note
    update_data = TradeNoteUpdate(reason="Updated Note")
    updated_note = update_note(db, test_note.id, update_data)  # Attempt to update
    assert updated_note is None, "Deleted notes should NOT be updated"


def test_soft_delete_note(db: Session, test_note):
    """Test soft deletion of a note"""
    soft_delete_note(db, test_note.id)
    deleted_note = get_note(db, test_note.id)
    assert deleted_note is None, "Soft-deleted notes should NOT be retrieved"
