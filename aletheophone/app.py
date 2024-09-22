from fastapi import FastAPI
from .controller.note import router as note_router
from .controller.stream import router as stream_router

app = FastAPI()

app.include_router(note_router)
app.include_router(stream_router)
