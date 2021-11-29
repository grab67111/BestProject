import os
import uuid

import aiohttp
import aiofiles
from aiofiles import os as a_os
import m3u8_To_MP4


async def parse_m3u8(url, fetcher):
    async with fetcher as session:
        filename = str(uuid.uuid4())
        async with session.get(url) as resp:
            if resp.status == 200:
                data = await resp.read()
            else:
                data = b''

    async with aiofiles.open(filename, mode='wb') as f:
        await f.write(data)

    try:
        async with aiofiles.open(filename) as f:
            async for line in f:
                if line.startswith('http'):
                    yield line.strip()
    finally:
        await a_os.remove(filename)


def download_to_mp4(url):
    filename = f'{uuid.uuid4()}.mp4'
    with open(filename, "w") as f:
        f.write("")

    try:
        m3u8_To_MP4.async_download(url, mp4_file_name=filename)
    finally:
        os.remove(filename)
