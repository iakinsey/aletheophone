from datetime import timedelta
from typing import Literal
from fastapi import Depends, Query
from pydantic import BaseModel
from ..deps import app, db
from ..model.note import Note


class CreateNoteRequest(BaseModel):
    text: str


@app.post("/note")
async def create_note(request: CreateNoteRequest, db=Depends(db)):
    note = Note()


@app.get("/note/{id}")
async def get_note(id: int, db=Depends(db)):
    return await db.fetch_one(Note.get(), (id,))


@app.delete("/note/{id}")
async def delete_note(id: int, db=Depends(db)):
    note = await db.fetch_one(Note.get(), (id,))

    if not note:
        raise KeyError(id)

    await db.execute(*note.delete())


@app.get("/notes")
async def get_notes(
    order_by: Literal["created", "vector"] = Query(
        "created", description="Field to order by"
    ),
    order: Literal["ASC", "DESC"] = Query("ASC", description="Order direction"),
    limit: int = Query(25, ge=1, le=100, description="Limit the number of results"),
    offset: int = Query(0, ge=0, description="Offset for the results"),
    window: timedelta = Query(
        timedelta(days=30), description="Time window for the notes"
    ),
    db=Depends(db),
) -> list[Note]:
    return await db.fetch(Note, Note.list(order_by, order, limit, offset, window))
