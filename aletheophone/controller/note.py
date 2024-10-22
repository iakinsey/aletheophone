from datetime import timedelta
from typing import Literal
from fastapi import APIRouter, Depends, Query, HTTPException
from pydantic import BaseModel
from ..deps import db
from ..gateway.data import DataGateway
from ..model.note import Note

router = APIRouter()


class CreateNoteRequest(BaseModel):
    text: str


@router.post("/note", response_model=Note)
async def create_note(
    request: CreateNoteRequest, db: DataGateway = Depends(db)
) -> Note:
    note = await db.fetch_one(Note, *(await Note.create(request.text)), commit=True)

    return note.model_dump()


@router.get("/note/{id}", response_model=Note)
async def get_note(id: int, db: DataGateway = Depends(db)) -> Note:
    note = await db.fetch_one(Note, *Note.get(id))

    if not note:
        raise HTTPException(status_code=404)

    return note.model_dump()


@router.delete("/note/{id}")
async def delete_note(id: int, db: DataGateway = Depends(db)):
    note = await db.fetch_one(Note, *Note.get(id))

    if not note:
        raise HTTPException(status_code=404)

    await db.execute(*note.delete())


@router.get("/notes")
async def get_notes(
    limit: int = Query(25, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: DataGateway = Depends(db),
) -> list[Note]:
    return [n.model_dump() for n in await db.fetch(Note, Note.list(limit, offset))]
