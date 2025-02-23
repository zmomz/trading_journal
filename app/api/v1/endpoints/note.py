from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.note import TradeNoteCreate, TradeNoteResponse
from app.crud.note import get_note, get_notes_by_trade, create_note
from typing import List

router = APIRouter(prefix="/notes", tags=["Trade Notes"])

@router.post("/", response_model=TradeNoteResponse)
def create_new_note(note: TradeNoteCreate, db: Session = Depends(get_db)):
    return create_note(db, note)

@router.get("/{note_id}", response_model=TradeNoteResponse)
def read_note(note_id: int, db: Session = Depends(get_db)):
    db_note = get_note(db, note_id)
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return db_note

@router.get("/trade/{trade_id}", response_model=List[TradeNoteResponse])
def read_trade_notes(trade_id: int, db: Session = Depends(get_db)):
    return get_notes_by_trade(db, trade_id)