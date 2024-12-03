from fastapi import APIRouter, HTTPException
from select import select
from starlette import status

from app.database import models
from app.schema.notes import NoteIn, NoteOut
from app.database.database import SessionDep
from app.database.models import Note
router = APIRouter(
    tags=['Notes'],
)

@router.post("/notes/", status_code=status.HTTP_201_CREATED)
async def create_note(note: NoteIn, session: SessionDep)-> NoteOut:
    note_in = Note(**note.dict())
    session.add(note_in)
    session.commit()
    session.refresh(note_in)
    return note_in



@router.get("/notes/", status_code=status.HTTP_200_OK)
async def get_note(session: SessionDep)-> list[NoteOut]:
    notes = session.query(models.Note).all()
    return notes


@router.put("/notes/{note_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_note(note_id: int, note_in: NoteIn, session: SessionDep)->NoteOut:
    note = session.get(Note, note_id)
    if not note:
       print("No  found notes")
    note.title = note_in.title
    note.content = note_in.content

    session.commit()
    return note


@router.delete("/notes/{note_id}/")
async def delete_note(note_id: int, session: SessionDep)->dict:
    note_db = session.query(models.Note).filter(models.Note.id == note_id).first()
    if not note_db:
        raise HTTPException(status_code=404, detail="Note not found")
    session.delete(note_db)
    session.commit()
    return {"status": True, "detail": "Note deleted"}


