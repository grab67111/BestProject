import json


class JsonWriterPipeline:
    def open_spider(self, spider):
        self.items = []

    def close_spider(self, spider):
        with open('data.json', 'w') as f:
            json.dump(self.items, f)

    def process_item(self, item, spider):
        self.items.append(item)
        return item
