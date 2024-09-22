from os import remove

from aiofiles import open as aopen
from aiofiles.tempfile import NamedTemporaryFile
from fastapi import Depends, WebSocket, WebSocketDisconnect
from fastapi import APIRouter
from whisper import load_model

from ..deps import db
from ..gateway.data import DataGateway
from ..model.note import Note


model = load_model("medium.en")
router = APIRouter()
term_char = "\ue784"


# TODO add a session ID so that streams can be continued in the event they break
@router.websocket("/stream")
async def voice_stream_processor(websocket: WebSocket, db: DataGateway = Depends(db)):
    await websocket.accept()

    async with NamedTemporaryFile(mode="w+b", delete=False) as f:
        window = bytearray()

        try:
            while True:
                data = await websocket.receive_bytes()

                try:
                    await f.write(data)
                except Exception as exc:
                    print(data)

                for byte in data:
                    window.append(byte)

                    if len(window) > 2:
                        window.pop(0)

                    if window == b"\x9E\x84":
                        await f.seek(-2, 2)
                        await f.truncate()

                        text = model.transcribe(f.name, language="english")[
                            "text"
                        ].strip()
                        params = await Note.create(text)
                        note = await db.fetch_one(Note, *params, commit=True)

                        await websocket.send_json(note.model_dump())
                        return
        except WebSocketDisconnect:
            pass
        except Exception as e:
            print(e)
