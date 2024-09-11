from fastapi import FastAPI
from .controller.note import router as note_router


app = FastAPI()

app.include_router(note_router)
