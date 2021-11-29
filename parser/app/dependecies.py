from .config.lazy import settings

from elasticsearch import AsyncElasticsearch


elastic = AsyncElasticsearch()
