from fastapi import APIRouter, Depends

from .services.fetcher import AsyncFetcher
from .services.parse import scrape_article


router = APIRouter()


def get_fetcher():
    return AsyncFetcher()


@router.post("/scrape")
async def scrape_page(url: str, fetcher: AsyncFetcher = Depends(get_fetcher)):
    article = await scrape_article(fetcher, url)
    return {"data": article}
