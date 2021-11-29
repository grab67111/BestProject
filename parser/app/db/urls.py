from datetime import datetime

from fastapi import APIRouter

from ..dependecies import elastic as es


router = APIRouter()

from loguru import logger

@router.post("/test")
async def test():
    doc = {
        'author': 'kimchy',
        'text': 'Elasticsearch: cool. bonsai cool.',
        'timestamp': datetime.now(),
    }
    res = await es.index(index="test-index", id=1, document=doc)
    logger.debug(res)
    return res


@router.get("/test2")
async def test2():
    res = await es.get(index="test-index", id=1)
    logger.debug(res)
    return res


@router.get("/test3")
async def test3():
    res = await es.search(index="test-index", query={"match_all": {}})
    logger.debug(res)
    return res
