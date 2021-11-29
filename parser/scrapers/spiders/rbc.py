import re

from bs4 import BeautifulSoup as bs
import scrapy
from scrapy import Selector
from loguru import logger

from ..services.m3u8 import parse_m3u8


url = "https://www.rbc.ru/"

AJAX_HOST = "https://www.rbc.ru/v10/ajax/get-news-by-filters/?offset="


class QuotesSpider(scrapy.Spider):
    name = "rbc"

    def start_requests(self):
        yield scrapy.Request(url=url, callback=self.parse)
        for offset in range(0, 1020, 20):
            if offset == 1020:
                yield scrapy.Request(url=url, callback=self.parse)
            yield scrapy.Request(url=(AJAX_HOST + str(offset)), callback=self.parse_ajax)


    def parse(self, response):
        news = response.css("a.news-feed__item::attr(href)").getall()
        for new in news:
            yield scrapy.Request(new, callback=self.parse_page)


    def parse_ajax(self, response):
        for addr in re.findall('https://w[./a-z0-9]+', response.text):
            yield scrapy.Request(addr, callback=self.parse_page)


    def parse_page(self, response):
        soup = bs(response.text, 'html.parser')

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

        try:
            videos = []
            for video in tuple(map(
                lambda x: x['data-shorturl'],
                soup.find_all(class_='js-insert-video')
            )):
                for url in parse_m3u8(video):
                    videos.append(url)
        except Exception:
            videos = tuple(map(
                lambda x: x['data-href'],
                soup.find_all(class_='js-insert-video')
            ))

        yield {
            'title': title,
            'body': body,
            'videos': videos,
            'imgs': imgs,
            'tags': tags,
            'url': response.url,
        }