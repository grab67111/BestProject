import io
import os
import uuid

from pydub import AudioSegment
from pydub.utils import make_chunks


class Converter:
    class Decorator:
        @staticmethod
        def transform(func) -> io.BytesIO:
            def wrapper(file: bytes, file_format: str, new_format: str):
                file = func(file, file_format)

                filename = f'{uuid.uuid4()}.{new_format}'
                file.export(filename, format=new_format)

                f = open(filename, 'rb')
                try:
                    return io.BytesIO(f.read())
                finally:
                    f.close()
                    os.remove(filename)
            return wrapper

    @staticmethod
    @Decorator.transform
    def from_file(file: bytes, file_format: str) -> AudioSegment:
        return AudioSegment.from_file(file, format=file_format)


class Slicer:
    chunks: list[AudioSegment]
    file_format: str = 'ogg'

    def __init__(self, file, file_format='ogg', seconds=0, minutes=0):
        self.file_format = file_format
        audio = AudioSegment.from_file(file, format=self.file_format)
        seconds += minutes * 60
        chunk_length_ms = seconds * 1000
        self.chunks = make_chunks(audio, chunk_length_ms)

    def __iter__(self):
        self.position = 0
        return self

    def __next__(self) -> bytes:
        if self.position == len(self.chunks):
            raise StopIteration

        else:
            filename = f'{uuid.uuid4()}.{self.file_format}'
            self.chunks[self.position].export(filename, format=self.file_format)
            f = open(filename, 'rb')
            try:
                return f.read()
            finally:
                self.position += 1
                f.close()
                os.remove(filename)
