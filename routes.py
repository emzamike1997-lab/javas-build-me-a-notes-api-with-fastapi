```python
# routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from . import database, models, schemas
from .utils import get_db

notes_router = APIRouter()

@notes_router.get("/notes/")
async def read_notes(db: AsyncSession = Depends(get_db)):
    notes = await db.query(models.Note).all()
    return notes

@notes_router.get("/notes/{note_id}")
async def read_note(note_id: int, db: AsyncSession = Depends(get_db)):
    note = await db.query(models.Note).filter(models.Note.id == note_id).first()
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@notes_router.post("/notes/")
async def create_note(note: schemas.NoteCreate, db: AsyncSession = Depends(get_db)):
    db_note = models.Note(title=note.title, content=note.content)
    db.add(db_note)
    await db.commit()
    await db.refresh(db_note)
    return db_note

@notes_router.put("/notes/{note_id}")
async def update_note(note_id: int, note: schemas.NoteUpdate, db: AsyncSession = Depends(get_db)):
    db_note = await db.query(models.Note).filter(models.Note.id == note_id).first()
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    db_note.title = note.title
    db_note.content = note.content
    db.add(db_note)
    await db.commit()
    await db.refresh(db_note)
    return db_note

@notes_router.delete("/notes/{note_id}")
async def delete_note(note_id: int, db: AsyncSession = Depends(get_db)):
    note = await db.query(models.Note).filter(models.Note.id == note_id).first()
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    await db.delete(note)
    await db.commit()
    return {"message": "Note deleted successfully"}
```

###