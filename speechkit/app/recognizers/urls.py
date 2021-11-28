from functools import partial
from typing import Optional

from fastapi import APIRouter, Depends
from fastapi import File, UploadFile

from ..dependecies import SPEECHKITS, ws_manager

from .services.audio import Slicer, Converter
from .models.chunk import Chunk


router = APIRouter()


async def converter_io(file: UploadFile = File(...)):
    fileformat = file.filename.split('.')[-1]
    return partial(Converter.from_file, file.file, fileformat)


@router.post("/recognize")
async def recognize(
    speech_model: str,
    converter: UploadFile = Depends(converter_io),
    user_id: Optional[int] = None,
):
    speechkit = SPEECHKITS[speech_model]['adapter']
    file = converter(SPEECHKITS[speech_model]['format'])

    chunks = [Chunk([''], is_final=False)]
    for bytes_content in Slicer(file, minutes=5):
        for chunk in speechkit.recognize(bytes_content):
            chunks.append(chunk)
            if user_id:
                await ws_manager.send_personal_json(chunk.to_dict(), user_id)

    final_chunks = tuple(filter(lambda x: x.is_final, chunks))
    final_text = ' '.join((i.alternatives[0] for i in final_chunks))
    if user_id:
        await ws_manager.send_personal_message(final_text, user_id)
    return {"data": final_text}
