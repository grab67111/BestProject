import json

from loguru import logger


class JsonWriterPipeline:
    def open_spider(self, spider):
        logger.success(f'{spider}: started!')
        self.items = []

    def close_spider(self, spider):
        logger.success(f'{spider}: finished!')
        with open('data.json', 'w') as f:
            json.dump(self.items, f)
        logger.success(f'{len(self.items)} articles were saved!')

    def process_item(self, item, spider):
        self.items.append(item)
        logger.info(item['title'])
        return item
