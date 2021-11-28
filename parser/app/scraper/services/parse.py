from bs4 import BeautifulSoup as bs

from ..models.article import Article
from .fetcher import AsyncFetcher


async def scrape_article(fetcher: AsyncFetcher, url: str) -> Article:
    soup = bs(await fetcher.get_text(url), 'html.parser')

    title = soup.find(class_="article__header__title").text
    imgs = tuple(map(
        lambda x: x['src'],
        soup.find_all('img')
    ))
    videos = tuple(map(
        lambda x: x['data-shorturl'],
        soup.find_all(class_='js-insert-video')
    ))
    body = ' '.join(tuple(map(
        lambda x: x.text,
        soup.find_all("div", class_="article__content")
    )))
    tags = tuple(map(
        lambda x: x.text,
        soup.find_all(class_="article__tags__item")
    ))

    return Article(
        title=title, body=body,
        images=imgs, videos=videos,
        tags=tags
    )
