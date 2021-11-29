BOT_NAME = 'scrapers'

SPIDER_MODULES = ['scrapers.spiders']
NEWSPIDER_MODULE = 'scrapers.spiders'

FEED_EXPORT_ENCODING = 'utf-8'

ROBOTSTXT_OBEY = True

DOWNLOAD_FAIL_ON_DATALOSS = True

LOG_ENABLED = False

ITEM_PIPELINES = {
    'scrapers.pipelines.JsonWriterPipeline': 300,
}