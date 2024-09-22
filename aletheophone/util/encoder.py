from asyncio import get_running_loop
from concurrent.futures import ThreadPoolExecutor
from numpy import ndarray
from sentence_transformers import SentenceTransformer


class Encoder:
    def __init__(self):
        self.model_name = "dunzhang/stella_en_1.5B_v5"
        self.model = SentenceTransformer(self.model_name)
        self.pool = ThreadPoolExecutor(max_workers=4)

    async def encode(self, strings: str) -> ndarray:
        loop = get_running_loop()
        return await loop.run_in_executor(self.pool, self.model.encode, strings)
