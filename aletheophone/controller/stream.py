from asyncio import run, Future
from os import remove
from tempfile import NamedTemporaryFile

from aiofiles import open as aopen
from websockets import serve, ConnectionClosed
import whisper


model = whisper.load_model("medium.en")


async def audio_handler(websocket, path):
    path = NamedTemporaryFile(delete=False).name

    try:
        async with aopen(path, mode="wb") as f:
            while 1:
                await f.write(await websocket.recv())
    except ConnectionClosed:
        out = model.transcribe(path, language="english")
        print(out["text"])
    finally:
        remove(path)


async def main():
    # Start the WebSocket server
    async with serve(audio_handler, "localhost", 8765):
        print("Server started, waiting for connections...")
        await Future()  # Run forever


if __name__ == "__main__":
    run(main())
