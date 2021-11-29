from multiprocessing import Process

from fastapi import APIRouter, Depends

from twisted.internet.error import ReactorAlreadyRunning

from .services.fetcher import AsyncFetcher
from .services.parse import scrape_article
from ..dependecies import scrapy_process


router = APIRouter()


def get_fetcher():
    return AsyncFetcher()


@router.post("/scrape")
async def scrape(url: str, fetcher: AsyncFetcher = Depends(get_fetcher)):
    article = await scrape_article(fetcher, url)
    return {"data": article}


@router.post("/run")
async def runner():
    try:
        scrapy_process.crawl('rbc')
        p = Process(target=scrapy_process.start(stop_after_crawl=False))
        p.start()
    except ReactorAlreadyRunning:
        pass
    return 200
