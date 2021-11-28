from typing import Generator

from ..models.chunk import Chunk
from ..models.speechkit_usecase import SpeechkitUsecase


class KaldiAdapter(SpeechkitUsecase):
    def recognize(self, file: bytes, chunk_size: int = 4000) -> Generator[Chunk, None, Chunk]:
        yield Chunk([""], is_final=False)