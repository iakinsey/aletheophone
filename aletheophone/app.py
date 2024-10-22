from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .controller.note import router as note_router
from .controller.stream import router as stream_router

app = FastAPI()

app.include_router(note_router)
app.include_router(stream_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
