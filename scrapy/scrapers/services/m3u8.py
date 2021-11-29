import os
import uuid

import requests
import m3u8_To_MP4


def parse_m3u8(url):
    filename = str(uuid.uuid4())
    resp = requests.get(url)
    if resp.status_code == 200:
        data = resp.content
    else:
        data = b''

    with open(filename, mode='wb') as f:
        f.write(data)

    try:
        with open(filename) as f:
            for line in f:
                if line.startswith('http'):
                    yield line.strip()
    finally:
        os.remove(filename)


def download_to_mp4(url):
    filename = f'{uuid.uuid4()}.mp4'
    with open(filename, "w") as f:
        f.write("")

    try:
        m3u8_To_MP4.async_download(url, mp4_file_name=filename)
    finally:
        os.remove(filename)
