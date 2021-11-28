from typing import Generator

import grpc
from loguru import logger

from ..models.chunk import Chunk
from ..models.speechkit_usecase import SpeechkitUsecase

from .yandex_streaming.yandex.cloud.ai.stt.v2 import stt_service_pb2 as stt_service_pb2
from .yandex_streaming.yandex.cloud.ai.stt.v2 import stt_service_pb2_grpc as stt_service_pb2_grpc


class YandexAdapter(SpeechkitUsecase):
    api_key: str

    def __init__(self, api_key):
        self.api_key = api_key
        self.short_file_request_params = {
            'headers': {
                'Authorization': f"Api-Key {api_key}"
            },
            'params': {
                "topic": "general",
                "lang": "ru-RU"
            },
            'url': "https://stt.api.cloud.yandex.net/speech/v1/stt:recognize"
        }
        specification = stt_service_pb2.RecognitionSpec(
            language_code='ru-RU',
            model='general',
            partial_results=True,
        )
        self.streaming_config = stt_service_pb2.RecognitionConfig(specification=specification)


    def recognize(self, file: bytes, chunk_size: int = 4000) -> Generator[Chunk, None, Chunk]:
        cred = grpc.ssl_channel_credentials()
        channel = grpc.secure_channel('stt.api.cloud.yandex.net:443', cred)
        stub = stt_service_pb2_grpc.SttServiceStub(channel)

        it = stub.StreamingRecognize(
            self._gen(file, chunk_size),
            metadata=(
                ('authorization', f'Api-Key {self.api_key}'),
            )
        )

        try:
            for r in it:
                yield Chunk(
                    alternatives=[i.text for i in r.chunks[0].alternatives],
                    is_final=r.chunks[0].final
                )
        except grpc._channel._Rendezvous as err:
            logger.error(f'Error code {err._state.code}, message: {err._state.details}')


    def _gen(self, file: bytes, chunk_size: int):
        yield stt_service_pb2.StreamingRecognitionRequest(config=self.streaming_config)

        data = file[:chunk_size]
        file = file[chunk_size:]
        while data != b'':
            yield stt_service_pb2.StreamingRecognitionRequest(audio_content=data)
            data = file[:chunk_size]
            file = file[chunk_size:]
