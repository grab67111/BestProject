from io import IOBase

from typing import Generator, Protocol

from .chunk import Chunk


class SpeechkitUsecase(Protocol):
    def recognize(self, file: IOBase, chunk_size: int) -> Generator[Chunk, None, Chunk]:
        raise NotImplementedError()
