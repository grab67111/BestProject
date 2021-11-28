import asyncio
from json.decoder import JSONDecodeError
from typing import Optional

import aiohttp
from aiohttp.client_exceptions import (
    ServerTimeoutError, ClientHttpProxyError,
    ClientProxyConnectionError, ContentTypeError,
    ClientOSError, ServerDisconnectedError
)
from loguru import logger


class MaxRetriesExceeded(Exception):
    def __init__(self, max_tries: int, message: Optional[str] = None):
        if message is None:
            message = f"Max retries '{max_tries}' exceeded"
        super().__init__(message)


def session_mixin(func):
    async def wrapper(self, url, *args, **kwargs):
        for try_number in range(self._max_retries):

            try:
                if session := kwargs.pop('session', self._session):
                    return await func(self, url, *args, session=session, **kwargs)

                else:
                    async with aiohttp.ClientSession() as session:
                        return await func(self, url, *args, session=session, **kwargs)

            except (ServerTimeoutError, asyncio.exceptions.TimeoutError, ServerDisconnectedError):
                logger.error(f'Timeout error {url}')
                await self.sleep()
                continue

            except (ClientHttpProxyError, ClientProxyConnectionError):
                logger.error(f'Proxy error {url}')
                await self.sleep()
                continue

            except (ContentTypeError, JSONDecodeError):
                logger.error(f'Сработала защита от ботов {url}')
                await self.sleep()
                continue

        raise MaxRetriesExceeded(self._max_retries)
    return wrapper


class AsyncFetcher:
    _max_retries: int
    _sleep_time: int
    _timeout_time: int
    _headers: dict

    _session: Optional[aiohttp.ClientSession] = None

    def __init__(self,
        max_retries=3, sleep=5,
        timeout=10, headers={
            'User-Agent': 'ozonapp_android/12.5+1425'
        },
    ):
        self._max_retries = max_retries
        self._sleep_time = sleep
        self._timeout_time = timeout
        self._headers = headers

    async def __aenter__(self, *args, **kwargs):
        self._session = aiohttp.ClientSession(*args, **kwargs)
        return self._session

    async def __aexit__(self, *args, **kwargs):
        if self._session is not None:
            await self._session.close()
        self._session = None

    @session_mixin
    async def get(self, url, *args, session, **kwargs):
        async with session.get(
            url, *args,
            headers=kwargs.pop('headers', self._headers),
            timeout=kwargs.pop('timeout', self._timeout_time),
            **kwargs
        ) as response:
            return response

    @session_mixin
    async def post(self, url, *args, session, **kwargs):
        async with session.post(
            url, *args,
            headers=kwargs.pop('headers', self._headers),
            timeout=kwargs.pop('timeout', self._timeout_time),
            **kwargs
        ) as response:
            return response

    @session_mixin
    async def get_text(self, url, *args, session, **kwargs):
        async with session.get(
            url, *args,
            headers=kwargs.pop('headers', self._headers),
            timeout=kwargs.pop('timeout', self._timeout_time),
            **kwargs
        ) as response:
            return await response.text()

    @session_mixin
    async def get_json(self, url, *args, session, check_content_type: bool = True, **kwargs):
        async with session.get(
            url, *args,
            headers=kwargs.pop('headers', self._headers),
            timeout=kwargs.pop('timeout', self._timeout_time),
            **kwargs
        ) as response:
            if check_content_type:
                try:
                    return await response.json()
                except (ContentTypeError, JSONDecodeError) as e:
                    if 'text/plain; charset=utf-8' in e.message:
                        logger.error('Wrong server response header. Needs to use "check_content_type=False" option')
                        return
                    else:
                        raise e
            else:
                return await response.json(content_type=None)

    async def sleep(self):
        await asyncio.sleep(self._sleep_time)
