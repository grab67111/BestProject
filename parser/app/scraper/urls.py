from fastapi import APIRouter, Depends

from loguru import logger

from .services.fetcher import AsyncFetcher
from .services.parse import scrape_article


router = APIRouter()


def get_fetcher():
    return AsyncFetcher()


@router.post("/scrape")
async def scrape(url: str, fetcher: AsyncFetcher = Depends(get_fetcher)):
    article = await scrape_article(fetcher, url)
    return {"data": article}
