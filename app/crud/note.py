from sqlalchemy.orm import Session
from app.models.note import TradeNote
from app.schemas.note import TradeNoteCreate, TradeNoteUpdate

def create_note(db: Session, note_data: TradeNoteCreate):
    """Create a new trade note."""
    db_note = TradeNote(**note_data.model_dump())
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

def get_note(db: Session, note_id: int):
    """Retrieve a trade note by ID, excluding soft-deleted notes."""
    return db.query(TradeNote).filter(TradeNote.id == note_id, TradeNote.deleted == False).first()

def get_notes_by_trade(db: Session, trade_id: int):
    """Retrieve all notes for a specific trade, excluding soft-deleted ones."""
    return db.query(TradeNote).filter(TradeNote.trade_id == trade_id, TradeNote.deleted == False).all()


def update_note(db: Session, note_id: int, note_data: TradeNoteUpdate):
    """Update an existing note only if it is not deleted and fields are provided."""
    db_note = db.query(TradeNote).filter(TradeNote.id == note_id, TradeNote.deleted == False).first()
    
    if not db_note:
        return None  # ✅ Ensure deleted notes are NOT updated

    update_fields = note_data.model_dump(exclude_unset=True)

    # ✅ Ensure `trade_id` is ignored during updates
    update_fields.pop("trade_id", None)  

    if not update_fields:
        return db_note  # No fields to update, return original

    for key, value in update_fields.items():
        setattr(db_note, key, value)

    db.commit()
    db.refresh(db_note)

    return db_note





def soft_delete_note(db: Session, note_id: int):
    """Soft delete a note (mark as deleted instead of removing)."""
    db_note = db.query(TradeNote).filter(TradeNote.id == note_id).first()
    if db_note:
        db_note.deleted = True
        db.commit()
    return db_note
