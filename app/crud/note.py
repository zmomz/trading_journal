from sqlalchemy.orm import Session
from app.models.note import TradeNote
from app.schemas.note import TradeNoteCreate
from datetime import datetime

def get_note(db: Session, note_id: int):
    return db.query(TradeNote).filter(TradeNote.id == note_id).first()

def get_notes_by_trade(db: Session, trade_id: int):
    return db.query(TradeNote).filter(TradeNote.trade_id == trade_id).all()

def create_note(db: Session, note: TradeNoteCreate):
    db_note = TradeNote(
        trade_id=note.trade_id,
        reason=note.reason,
        market_condition=note.market_condition,
        emotional_state=note.emotional_state,
        mistakes_lessons=note.mistakes_lessons,
        created_at=datetime.utcnow()
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note
