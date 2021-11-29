from .config.lazy import settings

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


scrapy_process = CrawlerProcess(get_project_settings())
