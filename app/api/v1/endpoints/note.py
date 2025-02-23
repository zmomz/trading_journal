from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.note import TradeNoteCreate, TradeNoteUpdate, TradeNoteResponse
from app.crud.note import create_note, get_note, get_notes_by_trade, update_note, soft_delete_note

router = APIRouter(prefix="/notes", tags=["Trade Notes"])

@router.post("/", response_model=TradeNoteResponse)
def create_trade_note(note_data: TradeNoteCreate, db: Session = Depends(get_db)):
    return create_note(db, note_data)

@router.get("/{note_id}", response_model=TradeNoteResponse)
def read_trade_note(note_id: int, db: Session = Depends(get_db)):
    note = get_note(db, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Trade note not found")
    return note

@router.get("/trade/{trade_id}", response_model=list[TradeNoteResponse])
def read_notes_for_trade(trade_id: int, db: Session = Depends(get_db)):
    return get_notes_by_trade(db, trade_id)

@router.patch("/{note_id}", response_model=TradeNoteResponse)
def update_trade_note(note_id: int, note_data: TradeNoteUpdate, db: Session = Depends(get_db)):
    note = update_note(db, note_id, note_data)
    if not note:
        raise HTTPException(status_code=404, detail="Trade note not found")
    return note

@router.delete("/{note_id}")
def delete_trade_note(note_id: int, db: Session = Depends(get_db)):
    note = soft_delete_note(db, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Trade note not found")
    return {"message": "Trade note deleted"}
