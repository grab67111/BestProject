from bs4 import BeautifulSoup as bs

from ..models.article import Article
from .fetcher import AsyncFetcher
from .m3u8 import parse_m3u8, download_to_mp4


async def scrape_article(fetcher: AsyncFetcher, url: str) -> Article:
    soup = bs(await fetcher.get_text(url), 'html.parser')

    title = soup.find(class_="article__header__title").text
    imgs = tuple(map(
        lambda x: x['src'],
        soup.find_all('img')
    ))
    body = ' '.join(tuple(map(
        lambda x: x.text,
        soup.find_all("div", class_="article__content")
    )))
    tags = tuple(map(
        lambda x: x.text,
        soup.find_all(class_="article__tags__item")
    ))

    videos = []
    for video in tuple(map(
        lambda x: x['data-shorturl'],
        soup.find_all(class_='js-insert-video')
    )):
        async for url in parse_m3u8(video, fetcher):
            videos.append(url)
    # download_to_mp4(videos[-1])

    return Article(
        title=title, body=body,
        images=imgs, videos=videos,
        tags=tags
    )
